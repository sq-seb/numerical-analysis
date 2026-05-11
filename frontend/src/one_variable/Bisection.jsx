import { useState, useRef, useEffect } from "react";
import { useForm } from "react-hook-form";
import parse from "./parser";
import { useMutation } from "@tanstack/react-query";

export default function Bisection() {
  const [error, setError] = useState("");
  const [errorKey, setErrorKey] = useState(0);

  const [showGrammar, setShowGrammar] = useState(false);

  const errorTimeoutRef = useRef(null);
  const lastSubmitValidRef = useRef(false);

  const resultRef = useRef(null);

  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      f: "",
      a: "",
      b: "",
      niter: "",
      value: "",
      tol_type: "DC",
    },
  });

  const API_URL = import.meta.env.VITE_API_URL;

  // ================= ERROR HANDLER =================
  const showError = (msg) => {
    if (lastSubmitValidRef.current) return;

    setError(msg);
    setErrorKey((k) => k + 1);

    if (errorTimeoutRef.current) {
      clearTimeout(errorTimeoutRef.current);
    }

    errorTimeoutRef.current = setTimeout(() => {
      setError("");
      errorTimeoutRef.current = null;
    }, 3000);
  };

  const blockInvalidKeys = (e) => {
    if (["-", "+", ".", "e", "E"].includes(e.key)) {
      e.preventDefault();
    }
  };

  const handleNiterChange = (e) => {
    let val = e.target.value;

    val = val.replace(/[^\d]/g, "");
    if (val === "0") val = "";

    setValue("niter", val);
  };

  // ================= VALIDATION =================
  const validateSyntax = (expr) => {
    try {
      parse(expr);
      return true;
    } catch {
      return false;
    }
  };

  // ================= MUTATION =================
  const mutation = useMutation({
    mutationFn: async (payload) => {
      const res = await fetch(`${API_URL}/bisection`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const json = await res.json();

      if (!res.ok) {
        throw new Error(json?.message || `Server error: ${res.status}`);
      }
      return json;
    },
    onError: e => {console.log(e)},
  });

  useEffect(() => {
    if (!mutation.data || !resultRef.current) return;

    const scroll = () => {
      const yOffset = -80; // 👈 adjust this (bigger = higher above)
      const element = resultRef.current;
      const y =
        element.getBoundingClientRect().top +
        window.pageYOffset +
        yOffset;

      window.scrollTo({
        top: y,
        behavior: "smooth",
      });
    };

    const id = requestAnimationFrame(() => {
      requestAnimationFrame(scroll);
    });

    return () => cancelAnimationFrame(id);
  }, [mutation.data]);

  const onSubmit = (data) => {
    lastSubmitValidRef.current = false;
    setError("");

    const niter = Number(data.niter);
    const tolValue = Number(data.value);

    if (!data.f) return showError("f(x) is required.");

    if (!validateSyntax(data.f)) {
      return showError(
        "Invalid mathematical expression for f(x). Click (?) for help."
      );
    }

    if (data.a === "") return showError("a is required.");
    if (data.a.length >= 16) return showError("a must not contain more than 16 figures.");

    if (data.b === "") return showError("b is required.");
    if (data.a.length >= 16) return showError("b must not contain more than 16 figures.");

    if (!Number.isInteger(niter) || niter < 1) {
      return showError("niter must be ≥ 1.");
    }

    if (data.value === "" || isNaN(tolValue)) {
      return showError("tolerance value is required.");
    }

    if (!Number.isInteger(tolValue)) {
      return showError("DC or CS must be an integer");
    }

    if (tolValue < 1 || tolValue > 15) {
      return showError("DC or CS must be in [1, 15]");
    }

    lastSubmitValidRef.current = true;

    const payload = {
      f: data.f,
      a: Number(data.a),
      b: Number(data.b),
      niter,
      tol_type: data.tol_type,
      value: tolValue,
    };

    mutation.mutate(payload);
  };

  return (
    <div className="w-full flex justify-center">
      <div className="w-full max-w-3xl">

        {/* ================= MODAL ================= */}
        {showGrammar && (
          <div
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
            onClick={() => setShowGrammar(false)}
          >
            <div
              className="bg-white text-black p-6 rounded-xl shadow-2xl max-w-xl w-full relative font-mono max-h-[80vh] overflow-y-auto animate__animated animate__zoomInDown"
              onClick={(e) => e.stopPropagation()}
            >
              {/* close button */}
              <button
                onClick={() => setShowGrammar(false)}
                className="absolute top-2 right-3 text-black text-xl font-bold hover:text-red-500 cursor-pointer"
              >
                ×
              </button>

              <h2 className="text-lg font-bold mb-3">f(x) must obey the following BNF grammar:</h2>

              <pre className="text-sm whitespace-pre-wrap">
{`<expr> ::= <term> { ("+" | "-") <term> }

<term> ::= <power> { ("*" | "/") <power> }

<power> ::= <unary> { "^" <unary> }

<unary> ::= "-" <unary>
          | <primary>

<primary> ::= <number>
            | <variable>
            | <function> "(" <expr> ")"
            | "(" <expr> ")"

<number> ::= <integer> 
          | <floating-point> 
          | <constant>

<integer> ::= [0-9]+

<floating-point> ::= [0-9]+ "." [0-9]+

<constant> ::= "e" | "pi"

<variable> ::= "x"

<function> ::= "sin" | "cos" | "tan" | "log10" | "ln"

-------------------------
EXAMPLES:

1. x^2 + 3*x + 1

2. sin(x)

3. cos(x)^2 + sin(x)^2

4. ln(e^x)

5. log10(100) + x/2

6. -(x^2 + 3*x - 5)
`}
              </pre>
            </div>
          </div>
        )}

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="bg-amber-400 p-4 relative rounded-2xl shadow-2xl shadow-black/50 font-mono text-xl animate__animated animate__jackInTheBox"
        >

          {/* ================= VALIDATION ERROR ================= */}
          {error && (
            <div
              key={errorKey}
              className="absolute top-2 left-1/2 -translate-x-1/2 
              bg-red-400 text-black px-4 py-2 rounded 
              shadow-xl shadow-black/40 text-xl 
              animate__animated animate__headShake 
              cursor-default select-none"
            >
              {error}
            </div>
          )}

          {/* f(x) */}
          <div className="mb-3">
            <label className="font-bold mb-1 flex items-center gap-2">
              f(x):

              <button
                type="button"
                onClick={() => setShowGrammar(true)}
                className="w-6 h-6 flex items-center justify-center rounded-full bg-black text-amber-400 text-sm font-bold animate-pulse hover:scale-110 transition cursor-pointer"
              >
                ?
              </button>
            </label>

            <input
              type="text"
              {...register("f")}
              className="w-full border p-2 bg-white"
              placeholder="e.g. x^(3/5) * sin(x) - 2*x + log10(35) + e^(10x)"
            />
          </div>

          {/* a */}
          <div className="mb-3">
            <label className="block font-bold mb-1">a (lowerbound):</label>
            <input
              type="number"
              step="any"
              placeholder="must be a number of no more than 16 figures"
              {...register("a")}
              className="w-full border p-2 bg-white"
            />
          </div>

          {/* b */}
          <div className="mb-3">
            <label className="block font-bold mb-1">b (upperbound):</label>
            <input
              type="number"
              step="any"
              placeholder="must be a number of no more than 16 figures"
              {...register("b")}
              className="w-full border p-2 bg-white"
            />
          </div>

          {/* niter */}
          <div className="mb-3">
            <label className="block font-bold mb-1">
              niter (max. number of iterations):
            </label>

            <input
              type="number"
              step="1"
              onKeyDown={blockInvalidKeys}
              onChange={handleNiterChange}
              {...register("niter")}
              className="w-full border p-2 bg-white"
              placeholder="must be ≥ 1"
            />
          </div>

          {/* tol_type */}
          <div className="mb-4">
            <p className="font-bold mb-2">tolerance:</p>

            <div className="flex gap-6 mb-3">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="radio" value="DC" {...register("tol_type")} />
                <span>DC</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer">
                <input type="radio" value="CS" {...register("tol_type")} />
                <span>CS</span>
              </label>
            </div>

            <input
              type="number"
              step="any"
              {...register("value")}
              className="w-full border p-2 bg-white"
              placeholder="amount of DC or CS must be between 1 and 15"
            />
          </div>

          <button
            type="submit"
            disabled={mutation.isPending}
            className="border cursor-pointer rounded-sm
            transition-transform duration-200 ease-out overflow-hidden
            hover:-translate-x-1 hover:translate-y-1
            active:-translate-x-2.5 active:translate-y-2.5
            hover:bg-black hover:text-amber-400
            hover:shadow-[10px_-10px_0_rgba(255,126,0,0.9)]
            active:shadow-[15px_-15px_0_rgba(255,80,0,0.7)]
            animate__animated animate__pulse"
          >
            {mutation.isPending ? "loading..." : "submit"}
          </button>

        </form>

        {/* ================= RESULT ================= */}
        {mutation.isError && (
          <div className="mt-4 text-black font-mono animate__animated animate__shakeX">
            API error.
          </div>
        )}

        {/* ============ RESULT ========= */}
        {mutation.isSuccess && mutation.data && (
          <div ref={resultRef} className="mt-4 w-full flex justify-center">
            <div
              className="inline-block p-10 bg-amber-400 text-black font-mono
              rounded-2xl shadow-2xl shadow-black/50
              animate__animated animate__zoomInDown"
            >

              {/* SOL + WARNING SECTION */}
              <div className="mb-3 space-y-1 border-black/30 text-xl font-bold">
                <div>
                  <span className="font-bold">Sol: x = </span>
                  {mutation.data.sol ?? "Mmm..."}
                </div>

                <div>
                  <span className="font-bold">Warning: </span>
                  {mutation.data.warning ?? "No warnings"}
                </div>
              </div>

              {/* TABLE OR EMPTY STATE */}
              {Array.isArray(mutation.data.table) && mutation.data.table.length > 0 ? (
                <div className="rounded-xl shadow-[inset_0_0_12px_rgba(0,0,0,0.25)]">
                  <table className="border-collapse text-center bg-white rounded-xl text-xs">
                    <thead className="bg-black text-amber-400 text-xs">
                      <tr>
                        <th className="border px-2 py-1">n</th>
                        <th className="border px-2 py-1">xn</th>
                        <th className="border px-2 py-1">f(xn)</th>
                        <th className="border px-2 py-1">En</th>
                        <th className="border px-2 py-1">εn</th>
                        <th className="border px-2 py-1">εₙ₋₁</th>
                      </tr>
                    </thead>

                    <tbody>
                      {mutation.data.table.map((row, index) => (
                        <tr key={index} className="hover:bg-amber-100 transition-colors">
                          <td className="border px-2 py-1">{row.n}</td>
                          <td className="border px-2 py-1">{row.xn}</td>
                          <td className="border px-2 py-1">{row["f(xn)"]}</td>
                          <td className="border px-2 py-1">{row.En}</td>
                          <td className="border px-2 py-1">{row["εn"]}</td>
                          <td className="border px-2 py-1">{row["ε_{n-1}"]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-center text-sm italic mt-2">
                  No iteration table returned by the solver.
                </div>
              )}

            </div>
          </div>
        )}

      </div>
    </div>
  );
}