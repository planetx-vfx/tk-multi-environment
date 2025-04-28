[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/planetx-vfx/tk-multi-environment?include_prereleases)](https://github.com/planetx-vfx/tk-multi-environment) 
[![GitHub issues](https://img.shields.io/github/issues/planetx-vfx/tk-multi-environment)](https://github.com/planetx-vfx/tk-multi-environment/issues) 


# ShotGrid Environment App

[![Documentation](https://img.shields.io/badge/documentation-blue?style=for-the-badge)](https://github.com/planetx-vfx/tk-multi-environment)

An app that handles setting up environment variables at the startup of an engine.

> Supported engines: tk-houdini, tk-maya

tk-multi-environment is a Shotgun Toolkit app that allows you to add some logic to the startup process of the engine. At default, the app sets the frame range to the frame range found in the configuration. If one can't be found it will default to 1001-1240. This and other things can be configured through your Shotgun configuration. 

## Environment variables
- `SG_PROJECT_NAME`: Project name
- `SG_PROJECT_ROOT`: Project file root
- `SG_USER_NAME`: Current username
- `SG_USER_ID`: Current user id
- `SG_CONTEXT_TYPE`: Current context type (Asset, Sequence, Shot)
- `SG_CONTEXT_ID`: Current context id
- `SG_STEP`: Current step
- `SG_NAME`: File name (_main_)
- `SG_VERSION`: File version
- `SG_VERSION_S`: File version as string (`v{version}`)
- Asset context:
  - `SG_ASSET`: Asset name
  - `SG_ASSET_ROOT`: Asset file root
- Sequence context:
  - `SG_SEQUENCE`: Sequence name
  - `SG_SEQUENCE_ROOT`: Sequence file root
- Shot context:
  - `SG_SEQUENCE`: Sequence name
  - `SG_SHOT`: Shot name
  - `SG_SHOT_ROOT`: Shot file root

## Requirements

| ShotGrid version | Core version | Engine version |
|------------------|--------------|----------------|
| -                | v0.14.37     | -              |

## Configuration

### Hooks

| Name          | Description                  | Default value        |
|---------------|------------------------------|----------------------|
| `helper_hook` | Implements helper functions. | helper_{engine_name} |


### Templates

| Name                    | Description                       | Default value | Fields                   |
|-------------------------|-----------------------------------|---------------|--------------------------|
| `work_file_template`    | A template for the work file path |               | context, version, [name] |
| `context_root_template` | A template for the root directory |               |                          |


### Lists

| Name                 | Description                                        | Default value |
|----------------------|----------------------------------------------------|---------------|
| `field_variables`    | A list of variables to apply from ShotGrid fields. |               |
| `template_variables` | A list of variables to apply using templates.      |               |


