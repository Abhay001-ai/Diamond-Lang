// Documentation.jsx
import React from "react";
import "./Documentation.css";

function Documentation() {
  return (
    <div id="documentation" className="documentation">
      <h2>📘 Diamond Lang Documentation</h2>

      <p><strong>Overview:</strong></p>
      <p>
        Diamond Lang is a dynamically typed toy language made for fun. It's simple, desi-style, and expressive.
      </p>

      <h3>🪩 Program Structure</h3>
      <pre><code>
{`kaam dost hello()
    bata dost "Hello World"
bas dost`}
      </code></pre>

      <h3>🔤 Variables</h3>
      <p>Use <code>bana dost</code> to declare variables. Reassign like normal.</p>
      <pre><code>
{`bana dost a = 10
bana dost b = "Diamond"
a = a + 5`}
      </code></pre>

      <h3>🔢 Data Types</h3>
      <ul>
        <li><strong>Numbers</strong>: <code>10</code>, <code>3.14</code></li>
        <li><strong>Strings</strong>: <code>"hello"</code>, <code>'ok'</code></li>
        <li><strong>Booleans</strong>: <code>sahi</code>, <code>galat</code></li>
        <li><strong>Null</strong>: <code>khaali</code></li>
      </ul>
      <pre><code>
{`bana dost x = 25
bana dost msg = "yo"
bana dost flag = sahi
bana dost empty = khaali`}
      </code></pre>

      <h3>🔁 Loops</h3>
      <p>Use <code>jab tak dost (condition)</code> for while loops.</p>
      <pre><code>
{`bana dost i = 0
jab tak dost (i < 5)
    bata dost i
    i = i + 1
bas dost`}
      </code></pre>

      <h3>🔀 Conditionals</h3>
      <ul>
        <li><code>agar dost (cond)</code></li>
        <li><code>nahi to dost (cond)</code></li>
      </ul>
      <pre><code>
{`bana dost x = 10
agar dost x < 5
    bata dost "small"
nahi to dost 
      bata dost "large"
bas dost`}
      </code></pre>

      <h3>📦 Functions</h3>
      <pre><code>
{`kaam dost square(x)
    wapas dost x * x
bas dost

bana dost ans = bula dost square(5)
bata dost ans`}
      </code></pre>

      <h3>🔊 Output</h3>
      <pre><code>
{`bata dost "Hello"
likh dost "World"
bata dost 5 + 5`}
      </code></pre>
    </div>
  );
}

export default Documentation;
