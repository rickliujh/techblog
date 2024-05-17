# Quartz v4 with giscus

My personal Quartz v4 configuration with giscus integrated.

## Changes

1. original Footer replaced by new component Links and moved to the right pane 
2. base.scss sidebar flex-wrap changed in order to support Links displayed properly on mobile version
3. original Footer replaced with Comments component which integrated Quartz with giscus
4. giscus integrated with Quartz theme change event so that the comment section's theme will change accordingly when Quartz switching between light/dark mode
5. add giscus.json to prevent comment from blog being abused

To see the changes, please refer to this commit [feat: integrate giscus for comment system](https://github.com/rickliujh/techblog/commit/3a63084fc7643367adf99f0e1133672f791bd25b)

## New Comments
### Comments
Comments component with its inline script `giscus.inline.ts` is responsible to integrate with giscus system and loading comments by leaving a hook `<div>` element with class `giscus` as well as align giscus theme with blog darkmode switching.

It's doing so by listening event `nav` on window and custom event `change` on ToggleSwitch for update page comment and giscus theme accordingly.

It will ignore `index` which is main page url when `nav` event fired so that the main page of the blog will not shows comments.

See, (giscus.inline.ts)[https://github.com/rickliujh/techblog/blob/v4/quartz/components/scripts/giscus.inline.ts], and (Comments.tsx)[https://github.com/rickliujh/techblog/blob/v4/quartz/components/Comments.tsx].

### Links
Links component is a modified Footer component optimized for displaying links on right side pane due to the comments occupied the end of section of the page.

> [!note]
> On mobile version, the Links will appear on the top of the page just right down on the blog name due to the Quartz layout limitation.

## ctl.sh

ctl.sh is a shell script tool that helps you using quartz cli without install `node` environment in your local machine, by utilizing docker node image as a throw-away container. Using `ctl.sh` is encouraged since the origin quartz docker support is not good enough.

### Usage
`bash ctl.sh m` to show the menu
```
 QUARTZ CTL MENU
  Options:
   (0) perview | p => perview blog before publich
   (1) sync => sync blog to remote repository, or update quartz
   (2) sync --no-pull | sop => sync blog to remote repository but not update quartz
   (3) quartz | q => run any quartz support sub commands
```
As the instruction of the menu you can use `p` to run a local server to preview, equals to `npx quartz build --serve`, sop to update blog context but not update quartz, and any other command available for quartz cli is available in `ctl.sh` by using command `bash ctl.sh quartz [quartz sub-command]`.

Feel free to fork the repository if you want to use giscus with Quartz.
