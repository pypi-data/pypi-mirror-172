# Add Custom Pipeline Repository

To add a local content pacakge to the `ai-core-sdk` content package tooling the path to the content package definition has to be added to the environment variable `AI_CORE_CONTENT_SPECS`. To do this manually execute
```bash
export AI_CORE_CONTENT_SPECS=$AI_CORE_CONTENT_SPECS:$PWD/customContentPackage.yaml
```
in this directory or use our script `source add_package.sh`.

Afterwards run `aicore-content list` to check if it was added successfully (`sap-cv-additional-preparation-workflow`).
