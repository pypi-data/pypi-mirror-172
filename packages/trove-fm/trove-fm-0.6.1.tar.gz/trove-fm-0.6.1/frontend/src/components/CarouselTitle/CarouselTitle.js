
import React from "react"
import { EuiTitle } from "@elastic/eui"
import { motion, AnimatePresence } from "framer-motion"

const transitionDuration = 0.7

const transitionEase = [0.68, -0.55, 0.265, 1.55]

const statement = `For busy people who need their`


export default function CarouselTitle({ items, current, interval = 3000 }) {
  return (
    <AnimatedTitle>
      <EuiTitle>
        <TitleWrapper>
          {statement.split(" ").map((word, i) => (
            <h1 key={i}>{word}</h1>
          ))}
          <AnimatePresence exitBeforeEnter>
            <AnimatedCarouselTitle>
              {items.map((item, i) => {
                return (
                  current === i && (
                    <motion.span
                      key={i}
                      initial="top"
                      animate="present"
                      exit="bottom"
                      variants={{
                        top: { opacity: 0, y: -150 },
                        present: { opacity: 1, y: 0 },
                        bottom: { opacity: 0, y: 150 }
                      }}
                      transition={{ duration: transitionDuration, ease: transitionEase }}
                    >
                      {item.label}
                    </motion.span>
                  )
                )
              })}
              <div className="underline" />
            </AnimatedCarouselTitle>
          </AnimatePresence>
          <h1>cleaned.</h1>
        </TitleWrapper>
      </EuiTitle>
    </AnimatedTitle>
  )
}
