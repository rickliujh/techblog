# Quartz v4 with giscus

My personal Quartz v4 configuration with giscus integrated.

## Changes

1. original Footer replaced by new component Links and moved to the right pane 
2. base.scss sidebar flex-wrap changed in order to support Links displayed properly on mobile version
3. original Footer replaced with Comments component which integrated Quartz with giscus
4. giscus integrated with Quartz theme change event so that the comment section's theme will change accordingly when Quartz switching between light/dark mode
5. add giscus.json to prevent comment from blog being abused

To see the changes, please refer to this commit [feat: integrate giscus for comment system](https://github.com/rickliujh/techblog/commit/3a63084fc7643367adf99f0e1133672f791bd25b)

Feel free to fork the repository if you want to use giscus with Quartz.
