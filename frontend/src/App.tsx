import React from 'react';
import FunctionChart from './components/FunctionChart/FunctionChart';
import {BrowserRouter, Route, Router, Routes} from "react-router-dom";
import {Header} from "./components/Header/Header";
import {HomePage} from "./pages/HomePage";
import {ParametersPage} from "./pages/ParametersPage";

function App() {
    return (
        <BrowserRouter>
            <Header />
            <main className="main-content">
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/parameters" element={<ParametersPage />} />
                </Routes>
            </main>
        </BrowserRouter>
    );
};

export default App;
