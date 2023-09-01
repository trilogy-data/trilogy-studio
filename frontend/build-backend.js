// build-pyinstaller.js
const { exec } = require('child_process');
const path = require('path');

const parentDir = path.resolve(__dirname, '..')
// Replace 'your_script.py' with your actual Python script or entry point
const pythonScript = path.join(parentDir, 'backend/build.py');
// const pythonScript = '../backend/src/build.py';

const venvPath = path.join(parentDir, '.venv/bin/python');

// this is set in CI
const pythonPath = process.env.pythonLocation;
const pyInstallerCommand = pythonPath ? `${pythonPath}/python ${pythonScript}` : `${venvPath} ${pythonScript}`;



exec(pyInstallerCommand, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error}`);
    console.error(`PyInstaller Errors:\n${stderr}`);
    throw error;
  }
  console.error(`PyInstaller Errors:\n${stderr}`);
  console.log(`PyInstaller Output:\n${stdout}`);
  
});