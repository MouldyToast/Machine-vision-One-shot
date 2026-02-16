#!/bin/sh

brew install python@2
pip install --upgrade virtualenv

# clone visionui source
rm -rf /tmp/visionuiSetup
mkdir /tmp/visionuiSetup
cd /tmp/visionuiSetup
curl https://codeload.github.com/tzutalin/labelImg/zip/master --output visionui.zip
unzip visionui.zip
rm visionui.zip

# setup python3 space
virtualenv --system-site-packages  -p python3 /tmp/visionuiSetup/visionui-py3
source /tmp/visionuiSetup/visionui-py3/bin/activate
cd labelImg-master

# build visionui app
pip install py2app
pip install PyQt6 lxml
rm -rf build dist
python setup.py py2app -A
mv "/tmp/visionuiSetup/labelImg-master/dist/visionui.app" /Applications
# deactivate python3
deactivate
cd ../
rm -rf /tmp/visionuiSetup
echo 'DONE'
