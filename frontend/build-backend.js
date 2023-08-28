// build-pyinstaller.js
const { exec } = require('child_process');
const path = require('path');

const parentDir = path.resolve(__dirname, '..')
// Replace 'your_script.py' with your actual Python script or entry point
const pythonScript = path.join(parentDir, 'backend/build.py');
// const pythonScript = '../backend/src/build.py';

const pyInstallerCommand = `python ${pythonScript}`;

exec(pyInstallerCommand, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error}`);
    return;
  }
  console.log(`PyInstaller Output:\n${stdout}`);
  console.error(`PyInstaller Errors:\n${stderr}`);
});