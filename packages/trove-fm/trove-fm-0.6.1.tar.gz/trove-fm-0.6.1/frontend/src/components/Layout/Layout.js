
/*
The Layout component will render other components inside of it, so it's a good place to add
any global styles, themes, and other meta data inside our application.
*/

import React from "react"
import Container from 'react-bootstrap/Container';

import { Helmet } from "react-helmet"
import { Navbar } from "components"  

export default function Layout({ children }) {
  // const { toasts, removeToast } = useToasts()

  return (
    <React.Fragment>
        <Helmet>
            <meta charSet="utf-8" />
            <title>Trove Farmers Market</title>
            <link rel="canonical" href="https://trove.fm" />
        </Helmet>
        <Container>
            <Container className="navbar">
              <Navbar />
            </Container>
            <Container className="child">{children}</Container>
        </Container>
    </React.Fragment>
    )
}
