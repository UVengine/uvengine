let pyodide = null;

async function loadPyodideAndPackages() {
  pyodide = await loadPyodide();
  // Carga dependencias si se necesitan
  // await pyodide.loadPackage(['numpy']);
  await pyodide.loadPackage('micropip');
  await pyodide.runPythonAsync(`
import micropip
await micropip.install('jinja2')
await micropip.install("flamapy/flamapy-2.0.1-py3-none-any.whl", deps=False)
await micropip.install("flamapy/flamapy_fw-2.0.2.dev0-py3-none-any.whl", deps=False)
await micropip.install("flamapy/flamapy_fm-2.0.2.dev0-py3-none-any.whl", deps=False)
await micropip.install("flamapy/flamapy_sat-2.0.1-py3-none-any.whl", deps=False)
await micropip.install("flamapy/flamapy_bdd-2.0.1-py3-none-any.whl", deps=False)
await micropip.install("flamapy/dd-0.5.7-py3-none-any.whl", deps=False)
await micropip.install("flamapy/ply-3.11-py2.py3-none-any.whl", deps=False)
await micropip.install("flamapy/astutils-0.0.6-py3-none-any.whl", deps=False)
await micropip.install("flamapy/graphviz-0.20-py3-none-any.whl", deps=False)
await micropip.install("flamapy/uvlparser-2.0.1-py3-none-any.whl", deps=False)
await micropip.install("flamapy/afmparser-1.0.3-py3-none-any.whl", deps=False)
await micropip.install("flamapy/antlr4_python3_runtime-4.13.1-py3-none-any.whl", deps=False)
  `);
}

async function loadUVEngineToFS() {
  if (!pyodide.FS.analyzePath("/uvengine").exists) {
    pyodide.FS.mkdir("/uvengine");
  }

  if (!pyodide.FS.analyzePath("/uvengine/utils").exists) {
    pyodide.FS.mkdir("/uvengine/utils");
  }

  // Ficheros Python dentro de la carpeta uvengine
  const moduleFiles = ["__init__.py", 
                       "uvengine.py", 
                       "configuration.py", 
                       "mapping_model.py", 
                       "variation_point.py",
                       "utils/__init__.py",
                       "utils/utils.py"]; // Añade todos los .py que tengas

  for (const filename of moduleFiles) {
    const response = await fetch(`uvengine/${filename}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch uvengine/${filename}`);
    }
    const code = await response.text();
    pyodide.FS.writeFile(`/uvengine/${filename}`, code);
  }

  // Añadir / al sys.path para importar correctamente
  await pyodide.runPythonAsync(`
import sys
if "/uvengine" not in sys.path:
    sys.path.insert(0, "/")
`);
}

// Obtiene contenido de un fichero como Uint8Array
async function getFileContent(file) {
  return new Uint8Array(await file.arrayBuffer());
}

// Descomprime zip y escribe todos los ficheros en FS de Pyodide
async function unzipAndWriteToFS(file) {
  const arrayBuffer = await file.arrayBuffer();
  const zip = await JSZip.loadAsync(arrayBuffer);
  for (const [filename, zipEntry] of Object.entries(zip.files)) {
    if (!zipEntry.dir) {
      const content = await zipEntry.async("uint8array");
      pyodide.FS.writeFile(`/${filename}`, content);
      console.log(`Extracted ${filename} to FS`);
    }
  }
}

// Escribe un solo fichero en FS
async function writeFileToFS(file) {
  const content = await getFileContent(file);
  pyodide.FS.writeFile(`/${file.name}`, content);
  console.log(`Wrote ${file.name} to FS`);
}

// Limpia la raíz del FS virtual
function clearFS() {
  try {
    const files = pyodide.FS.readdir('/');
    for (const f of files) {
      if (f !== '.' && f !== '..') {
        try {
          pyodide.FS.unlink(`/${f}`);
        } catch {}
      }
    }
  } catch {}
}

// Función que ejecuta el UVEngine dentro de Pyodide
async function runUVEngine(featureModel, configFiles, templateFiles, mainTemplate, mappingFile) {
  // Construimos lista de nombres para pasar a python
  const configs = configFiles.map(f => `/${f.name}`);
  const templates = templateFiles.map(f => `/${f.name}`);
  const feature_model = `/${featureModel.name}`;
  const mapping = mappingFile ? `/${mappingFile.name}` : "None";

  // Python para ejecutar el motor
  const pythonCode = `
import os
import zipfile
from io import BytesIO

import uvengine

feature_model_path = "${feature_model}"
configs_path = ${JSON.stringify(configs)}
templates_paths = ${JSON.stringify(templates)}
mapping_model_filepath = ${mapping === "None" ? "None" : `"${mapping}"`}

uv = uvengine.UVEngine(
    feature_model_path=feature_model_path,
    configs_path=configs_path,
    templates_paths=templates_paths,
    mapping_model_filepath=mapping_model_filepath
)

resolved_templates = uv.resolve_variability()

# Guardamos los resultados en la FS
for path, content in resolved_templates.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Creamos ZIP con todos los ficheros resultado
memory_file = BytesIO()
with zipfile.ZipFile(memory_file, "w") as zf:
    for f in resolved_templates.keys():
        with open(f, "r", encoding="utf-8") as file:
            zf.writestr(f, file.read())
memory_file.seek(0)
result = memory_file.read()
  `;

  // Ejecutamos el código python y recuperamos el zip resultado (bytes)
  await pyodide.runPythonAsync(pythonCode);
  const result = pyodide.globals.get("result");
  return result;
}

// Descarga blob con nombre
function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

document.getElementById("upload-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  document.getElementById("output").innerText = "";

  if (!pyodide) {
    alert("Pyodide is not loaded yet. Please wait.");
    return;
  }

  clearFS();

  // Obtener ficheros de formulario
  const featureModelFile = document.getElementById("feature-model").files[0];
  if (!featureModelFile) {
    alert("Feature model file is required.");
    return;
  }

  const configsFiles = Array.from(document.getElementById("configs").files);
  if (configsFiles.length === 0) {
    alert("At least one config file or zip required.");
    return;
  }

  const templatesFiles = Array.from(document.getElementById("templates").files);
  if (templatesFiles.length === 0) {
    alert("At least one template file or zip required.");
    return;
  }

  const mainTemplateName = document.getElementById("main-template-name").value.trim();
  if (!mainTemplateName) {
    alert("Main template name is required.");
    return;
  }

  const mappingFiles = document.getElementById("mapping").files;
  const mappingFile = mappingFiles.length > 0 ? mappingFiles[0] : null;

  document.getElementById("output").innerText = "Writing files...";

  // Subir feature model
  await writeFileToFS(featureModelFile);

  // Subir configs, si es zip, descomprimir, si no solo escribir
  for (const f of configsFiles) {
    if (f.name.endsWith(".zip")) {
      await unzipAndWriteToFS(f);
    } else {
      await writeFileToFS(f);
    }
  }

  // Subir templates, zip o sueltos
  for (const f of templatesFiles) {
    if (f.name.endsWith(".zip")) {
      await unzipAndWriteToFS(f);
    } else {
      await writeFileToFS(f);
    }
  }

  // Subir mapping si hay
  if (mappingFile) {
    await writeFileToFS(mappingFile);
  }

  document.getElementById("output").innerText = "Running UVEngine, please wait...";

  try {
    const resultZipBytes = await runUVEngine(featureModelFile, configsFiles, templatesFiles, mainTemplateName, mappingFile);
    const blob = new Blob([resultZipBytes], { type: "application/zip" });
    downloadBlob(blob, "resolved_templates.zip");
    document.getElementById("output").innerText = "Process finished successfully! Download started.";
  } catch (err) {
    document.getElementById("output").innerText = `Error: ${err.message || err}`;
  }
});

window.addEventListener("load", async () => {
  document.getElementById("output").innerText = "Loading Pyodide, please wait...";
  await loadPyodideAndPackages();
  await loadUVEngineToFS();
  document.getElementById("output").innerText = "Pyodide loaded. UVEngine ready.";
});