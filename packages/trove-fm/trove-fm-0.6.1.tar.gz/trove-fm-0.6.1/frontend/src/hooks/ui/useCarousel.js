
import { useEffect, useRef, useState } from "react"

/*
We use React.useRef to give ourselves access to the timeout reference, and
create state for shouldAnimate to give ourselves the option to start/stop the animation if we need to.
We also return an object with all of the appropriate variables,
giving us access to any of the internals we might need.
*/

export function useCarousel(items, interval) {
  const timeoutRef = useRef()
  const [shouldAnimate, setShouldAnimate] = useState(true)
  const [current, setCurrent] = useState(0)

  useEffect(() => {
    const next = (current + 1) % items.length
    if (shouldAnimate) {
      timeoutRef.current = setTimeout(() => setCurrent(next), interval)
    }
    return () => clearTimeout(timeoutRef.current)
  }, [current, items.length, interval, shouldAnimate])

  return { current, setShouldAnimate, timeoutRef }
}
