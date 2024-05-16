import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/comments.scss"
import script from "./scripts/giscus.inline"

export default ((opts?: Options) => {
  const Comments: QuartzComponent = ({ displayClass, cfg }: QuartzComponentProps) => {
    return (
      <footer class={`${displayClass ?? "comments"}`}>
        <hr />
        <div class="giscus">
        </div>
      </footer>
    )
  }

  Comments.afterDOMLoaded = script
  Comments.css = style
  return Comments
}) satisfies QuartzComponentConstructor
