// build-pyinstaller.js
const { exec, execFile } = require('child_process');
const path = require('path');

const parentDir = path.resolve(__dirname, '..')
// Replace 'your_script.py' with your actual Python script or entry point
const pythonScript = path.join(parentDir, 'frontend/public/trilogy-studio-engine');
// const pythonScript = '../backend/src/build.py';

execFile(pythonScript)