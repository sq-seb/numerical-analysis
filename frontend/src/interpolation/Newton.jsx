import { useState, useRef, useEffect } from "react";
import { useForm, useFieldArray } from "react-hook-form";
import { useMutation } from "@tanstack/react-query";

export default function Newton() {
  const [error, setError] = useState("");
  const [errorKey, setErrorKey] = useState(0);

  const errorTimeoutRef = useRef(null);
  const lastSubmitValidRef = useRef(false);
  const resultRef = useRef(null);

  const { control, register, handleSubmit, watch } = useForm({
    defaultValues: {
      validationPercent: undefined,
      pairs: [
        { x: "", y: "" },
        { x: "", y: "" },
      ],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "pairs",
  });

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

  const limitDigits = (e) => {
    const value = e.target.value;
    const digits = value.replace("-", "").replace(".", "");

    if (digits.length > 15) {
      e.target.value = value.slice(0, -1);
    }
  };

  const mutation = useMutation({
    mutationFn: async (payload) => {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/newton`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Request failed");
      return res.json();
    },
  });

  const onSubmit = (data) => {
    const vp = Number(data.validationPercent);
    const pairs = data.pairs;

    lastSubmitValidRef.current = false;

    if (!data.validationPercent || ![0.1, 0.2, 0.3].includes(vp)) {
      return showError("Please choose a validation percentage.");
    }

    const invalid = pairs.some((p) => {
      const x = String(p.x);
      const y = String(p.y);

      const cleanX = x.replace("-", "").replace(".", "");
      const cleanY = y.replace("-", "").replace(".", "");

      return (
        x === "" ||
        y === "" ||
        isNaN(Number(p.x)) ||
        isNaN(Number(p.y)) ||
        cleanX.length > 15 ||
        cleanY.length > 15
      );
    });

    if (invalid) {
      return showError("Please fill in all slots");
    }

    const xs = pairs.map((p) => Number(p.x));

    if (new Set(xs).size !== xs.length) {
      return showError("All x values must be different.");
    }

    const n = pairs.length;
    const validationSize = Math.floor(n * vp);
    const trainingSize = n - validationSize;

    if (trainingSize < 2) {
      return showError(
        "Not enough training data (must have at least 2 training points).",
      );
    }

    lastSubmitValidRef.current = true;
    setError("");

    mutation.mutate(data);
  };

  const validationPercent = Number(watch("validationPercent")) || 0;
  const n = fields.length;

  const validationSize = Math.floor(n * validationPercent);
  const trainingSize = n - validationSize;

  const splitIdx = trainingSize;

  // UI-only display conversion (IMPORTANT CHANGE)
  const validationPercentDisplay = validationPercent * 100;

  useEffect(() => {
    if (!mutation.data || !resultRef.current) return;

    const scroll = () => {
      resultRef.current.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
    };

    const id = requestAnimationFrame(() => {
      requestAnimationFrame(scroll);
    });

    return () => cancelAnimationFrame(id);
  }, [mutation.data]);

  return (
    <div className="w-full flex justify-center">
      <div className="w-full max-w-3xl">
        {/* ================= FORM ================= */}
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="bg-amber-400 p-4 relative rounded-2xl shadow-2xl shadow-black/50 font-mono text-xl animate__animated animate__jackInTheBox"
        >
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

          {/* ================= VALIDATION HEADER ================= */}
          <div className="mb-4 text-black font-bold text-xl">
            <p className="mb-1">Validation %:</p>

            <div className="flex gap-4 mb-2">
              {[10, 20, 30].map((val) => (
                <label key={val} className="flex items-center gap-1">
                  <input
                    type="radio"
                    value={val / 100} // ✅ backend still receives 0.1 / 0.2 / 0.3
                    {...register("validationPercent", {
                      valueAsNumber: true,
                    })}
                  />
                  {val}% {/* ✅ UI only */}
                </label>
              ))}
            </div>

            {/* ================= SUMMARY ================= */}
            <div className="text-lg bg-black/10 p-2 rounded">
              <div>
                validation slots:{" "}
                <span className="font-bold">{validationSize}</span>
              </div>

              <div className="text-sm">
                Computed as floor({validationPercentDisplay}% × {n})
              </div>
            </div>
          </div>

          {/* ================= FIELDS ================= */}
          {fields.map((field, index) => {
            const isValidation = index >= splitIdx;

            return (
              <div key={field.id}>
                {index === splitIdx && (
                  <div className="my-2 border-t-2 border-black/60" />
                )}

                <div
                  className={`flex gap-2 mb-2 items-center text-xl animate__animated animate__fadeIn ${
                    isValidation ? "opacity-60" : ""
                  }`}
                >
                  <span className="w-10 text-black font-bold">x{index}:</span>

                  <input
                    type="number"
                    step="any"
                    onInput={limitDigits}
                    {...register(`pairs.${index}.x`, {
                      valueAsNumber: true,
                    })}
                    className="border p-1 w-24 bg-white text-xl"
                  />

                  <span className="w-10 text-black font-bold">y{index}:</span>

                  <input
                    type="number"
                    step="any"
                    onInput={limitDigits}
                    {...register(`pairs.${index}.y`, {
                      valueAsNumber: true,
                    })}
                    className="border p-1 w-24 bg-white text-xl"
                  />

                  <span className="ml-2 text-black font-bold">
                    {isValidation ? "(validation)" : "(training)"}
                  </span>

                  <div className="w-22.5 flex justify-end">
                    {index >= 2 ? (
                      <button
                        type="button"
                        onClick={() => remove(index)}
                        className="border cursor-pointer rounded-sm transition-transform duration-200 ease-out overflow-hidden hover:-translate-x-1 hover:translate-y-1 active:-translate-x-2.5 active:translate-y-2.5 hover:bg-white hover:text-red-500 hover:shadow-[10px_-10px_0_rgba(255,80,80,0.9)] active:shadow-[15px_-15px_0_rgba(255,80,80,0.7)] bg-red-400 text-black font-bold px-2 text-xl"
                      >
                        remove
                      </button>
                    ) : (
                      <div className="w-full h-9" />
                    )}
                  </div>
                </div>
              </div>
            );
          })}

          {/* ================= ACTIONS ================= */}
          <div className="flex gap-2 mt-3 text-xl">
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

            {fields.length < 10 && (
              <button
                type="button"
                onClick={() => append({ x: "", y: "" })}
                className="border cursor-pointer rounded-sm transition-transform duration-200 ease-out overflow-hidden hover:-translate-x-1 hover:translate-y-1 active:-translate-x-2.5 active:translate-y-2.5 hover:bg-white hover:text-blue-500 hover:shadow-[10px_-10px_0_rgba(73,157,208,0.9)] active:shadows-[15px_-15px_0_rgba(73,157,208,0.7)] bg-blue-500 text-white px-3 py-1 animate__animated animate__pulse"
              >
                add
              </button>
            )}
          </div>
        </form>

        {/* ================= RESULT ================= */}
        {mutation.isError && (
          <div className="mt-4 text-black font-mono animate__animated animate__shakeX">
            API error
          </div>
        )}

        {mutation.data && (
          <div
            ref={resultRef}
            className="mt-4 p-4 bg-amber-400 text-black font-mono text-sm 
            rounded-2xl shadow-2xl shadow-black/50 
            animate__animated animate__zoomInDown"
          >
            {/* IMAGE */}
            {mutation.data.image && (
              <div className="mb-4 rounded-xl overflow-hidden shadow-[inset_0_0_12px_rgba(0,0,0,0.25)]">
                <img
                  src={`data:image/png;base64,${mutation.data.image}`}
                  alt="graph"
                  className="w-full rounded-xl"
                />
              </div>
            )}

            {/* POLYNOMIAL */}
            <div className="whitespace-pre-wrap mb-3 font-bold text-xl">
              {mutation.data.polynomial}
            </div>

            {/* DOMAIN */}
            {mutation.data.domain && (
              <div className="text-xl font-bold border-t border-black/30 mt-5 pt-3">
                Domain =
                <span className="font-mono font-normal ml-2">
                  [{mutation.data.domain[0]}, {mutation.data.domain[1]}]
                </span>
              </div>
            )}

            {/* ERROR */}
            {mutation.data.error_inf !== undefined && (
              <div className="mt-2 pt-3 border-t border-black/30 text-xl font-bold">
                ||E||∞ = {mutation.data.error_inf}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
