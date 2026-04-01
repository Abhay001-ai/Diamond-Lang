// App.jsx
import React, { useState, useEffect } from "react";
import Editor from "@monaco-editor/react";
import "./App.css";
import * as monaco from "monaco-editor";
import Documentation from "./Documentation";
import logo from "./diamond.png";

function App() {
  const [code, setCode] = useState("");

  const [output, setOutput] = useState("");

    useEffect(() => {
    monaco.languages.register({ id: "diamond" });

    monaco.languages.setMonarchTokensProvider("diamond", {
      keywords: [
        "kaam","likh", "bas", "wapas", "bana", "bata", "dost", "bula", "agar", "warna", "jabtak"
      ],
      tokenizer: {
        root: [
          [/[a-zA-Z_]\w*/, {
            cases: {
              "@keywords": "keyword",
              "@default": "identifier"
            }
          }],
          [/\d+/, "number"],
          [/".*?"/, "string"],
          [/\s+/, "white"]
        ]
      }
    });

    monaco.editor.defineTheme("diamond-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "keyword", foreground: "FFA500", fontStyle: "bold" }, // 🔶 orange
      { token: "identifier", foreground: "A9DC76" }, // 🟢 green
      { token: "number", foreground: "FFD866" }, // 🟡 yellow
      { token: "string", foreground: "78DCE8" }, // 🔵 blue
    ],
    colors: {
      "editor.foreground": "#FFFFFF",
      "editor.background": "#1E1E1E"
    }
  });

  monaco.editor.setTheme("diamond-dark");
  }, []);

    const runCode = async () => {
    const res = await fetch("http://localhost:5000/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code }),
    });

    const data = await res.json();
    setOutput(data.output);
  };


  const clearCode = () => {
    setCode("");
    setOutput("");
  };

  return (
    <div className="container">
      <div className="header">
          <img src={logo} alt="Diamond Lang Logo" className="logo" />
      </div>
      <h1 className="title">Playground</h1>
      <div className="button-bar">
        <button className="run-btn" onClick={runCode}>Run</button>
        <button className="clear-btn" onClick={clearCode}>Clear</button>
      </div>
      <div className="editor-box">
        <Editor
          height="300px"
          language="diamond"
          theme="vs-dark"
          value={code}
          onChange={(value) => setCode(value)}
          options={{ fontSize: 16 }}
        />
      </div>
      <div className="output-box">
        {output && (
          <pre>
            Shandaar diamond 🎉
            {"\n"}
            {output}
          </pre>
        )}
      </div>
      <Documentation />
    </div>
  );
}

export default App;
