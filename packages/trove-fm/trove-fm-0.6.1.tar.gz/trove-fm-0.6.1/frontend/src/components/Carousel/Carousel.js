
import React from "react"
import { EuiPanel } from "@elastic/eui"
import { motion, AnimatePresence } from "framer-motion"

// See https://github.com/styled-components/styled-components/issues/1816
// regarding the '&&' work-around here, to enforce the porper style

const transitionDuration = 0.3

const transitionEase = [0.68, -0.55, 0.265, 1.55]

export default function Carousel({ items = [], current, interval = 3000, ...props }) {
  return (
    <CarouselWrapper {...props}>
      <AnimatePresence exitBeforeEnter>
        {items.map((item, i) =>
          current === i ? (
            <React.Fragment key={i}>
              <motion.div
                key={i}
                initial="left"
                animate="present"
                exit="right"
                variants={{
                  left: { opacity: 0, x: -70 },
                  present: { opacity: 1, x: 0 },
                  right: { opacity: 0, x: 70 }
                }}
                transition={{ duration: transitionDuration, ease: transitionEase }}
              >
                <StyledEuiPanel paddingSize="l">{item.content}</StyledEuiPanel>
              </motion.div>
            </React.Fragment>
          ) : null
        )}
      </AnimatePresence>
    </CarouselWrapper>
  )
}
