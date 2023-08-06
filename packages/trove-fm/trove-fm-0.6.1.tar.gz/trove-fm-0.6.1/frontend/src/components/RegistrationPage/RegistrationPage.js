
import React from "react"
import Container from 'react-bootstrap/Container';
import { RegistrationForm } from "../../components"

export default function RegistrationPage(){
    return (
      <Container className="cred-form-wrapper">
        <h4 className="form-header">Register your account</h4>
        <RegistrationForm />
      </Container>
    )
}
