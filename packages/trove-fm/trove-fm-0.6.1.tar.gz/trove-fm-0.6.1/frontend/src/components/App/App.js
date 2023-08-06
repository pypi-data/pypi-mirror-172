
import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom"
import {
  Layout,
  LoginPage,
  NotFoundPage,
  RegistrationConfirmation,
  RegistrationPage
} from "../../components"

// import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/registration" element={<RegistrationPage />} />
          <Route path="/registration/confirmation" element={<RegistrationConfirmation />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
