tk-multi-environment is a ShotGrid Toolkit app that allows you to add environment values to your engine based on
ShotGrid fields and templates from the current context.

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

## Example configuration

```yaml
settings.tk-multi-environment.houdini.shot_step:
  work_file_template: houdini_shot_work
  context_root_template: shot_root
  field_variables:
    - entity_type: Project
      variables:
        SG_PROJECT_CODE: sg_short_name
        SG_FPS: sg_frame_rate
  template_variables:
    - name: JOB
      template: shot_work_area_houdini
  location: "@apps.tk-multi-environment.location"
```