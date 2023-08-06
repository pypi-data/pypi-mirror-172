
import React, { useEffect, useState } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import Form from 'react-bootstrap/Form';
import { useNavigate } from "react-router-dom"

import { useMutation } from '@tanstack/react-query';

import { registerPerson } from '../../services/_apiClient'
// import { useLoginAndRegistrationForm } from "hooks/ui/useLoginAndRegistrationForm"

export default function RegistrationForm() {
  const [validated, setValidated] = useState(false);

  // const creds = {
  //   "new_person_creds": {
  //     "email_label": "home",
  //     "name_first": "Conrad",
  //     "name_last": "Brean",
  //     "password": "zW5BFjiTcW.ei3YQRVqQnuC",
  //     "username": "conrad.brean@icloud.com"
  //   }
  // }

  const mutation = useMutation(creds => {
    return registerPerson(creds)
  })

  const handleSubmit = (event) => {
    console.log('FORM SUBMITTED')
    const form = event.currentTarget;
    event.preventDefault()
    if (form.checkValidity() === false) {
      event.preventDefault();  
      event.stopPropagation();
    }
    setValidated(true);

    const registrationFormData = {};

    if (form.namePrefix.value) {
      registrationFormData["name_prefix"] = form.namePrefix.value
    }
    if (form.nameFirst.value) {
      registrationFormData["name_first"] = form.nameFirst.value      
    }
    if (form.nameLast.value) {
      registrationFormData["name_last"] = form.nameLast.value      
    }
    if (form.nameSuffix.value) {
      registrationFormData["name_suffix"] = form.nameSuffix.value
    }
    if (form.emailLabel.value) {
      registrationFormData["email_label"] = form.emailLabel.value
    }
    if (form.email.value) {
      registrationFormData["username"] = form.email.value
    }
    if (form.password.value) {
      registrationFormData["password"] = form.password.value
    }

    const creds = {"new_person_creds": {...registrationFormData}}

    console.log('CALLING API CLIENT')
    console.log("================= BREAK, BREAK, BREAK ====================")
    mutation.mutate(creds)
  }

  return (
    <Form className="cred-form" noValidate validated={validated} onSubmit={handleSubmit}>
      <Row className="mb-3">
        <Col xs lg="3">
          <Form.Group className="mb-3" controlId="formNamePrefix">
            <FloatingLabel controlId="floatingInput" label="Prefix" className="mb-3">
              <Form.Select name="namePrefix">
                <option>Select</option>
                <option value="Dr">Dr.</option>
                <option value="Mr">Mr.</option>
                <option value="Ms">Ms.</option>
                <option value="Miss">Miss</option>
                <option value="Mrs">Mrs.</option>
                <option value="Mx">Mx.</option>
              </Form.Select>
            </FloatingLabel>
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formNameFirst">
            <FloatingLabel controlId="floatingInput" label="First Name" className="mb-3">
              <Form.Control type="text" name="nameFirst" placeholder="First Name" />
            </FloatingLabel>
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formNameLast">
            <FloatingLabel controlId="floatingInput" label="Last Name" className="mb-3">
              <Form.Control type="text" name="nameLast" placeholder="Last Name" />
            </FloatingLabel>
          </Form.Group>
        </Col>
        <Col xs lg="2">
          <Form.Group className="mb-3" controlId="formNameSuffix">
            <FloatingLabel controlId="floatingInput" label="Suffix" className="mb-3">
              <Form.Control type="text" name="nameSuffix" placeholder="Suffix" />
            </FloatingLabel>
          </Form.Group>
        </Col>
      </Row>
      <Row className="mb-3">
        <Col xs lg="3">
          <Form.Group className="mb-3" controlId="formEmailLabel">
            <FloatingLabel controlId="floatingInput" label="Email Label" className="mb-3">
              <Form.Control type="text" name="emailLabel" placeholder="Email Label" />
            </FloatingLabel>
          </Form.Group>
        </Col>
        <Col>
          <Form.Group className="mb-3" controlId="formUsername">
            <FloatingLabel controlId="floatingInput" label="Email address" className="mb-3">
              <Form.Control type="email" name="email" placeholder="Enter email" />
              <Form.Text className="text-muted">
                This will be your username.
              </Form.Text>
            </FloatingLabel>
          </Form.Group>
        </Col>
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <FloatingLabel controlId="floatingInput" label="Password" className="mb-3">
            <Form.Control type="password" name="password" placeholder="Password" />
          </FloatingLabel>
        </Form.Group>
      </Row>
      <Form.Group className="mb-3" controlId="formBasicCheckbox">
        <Form.Check type="checkbox" name="tncCheckbox" label="I agree to the Terms and Conditions." />
      </Form.Group>
      <Button variant="primary" type="submit">
        Submit
      </Button>
    </Form>
  );
}
