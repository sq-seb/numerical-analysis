export default function Card({ title, linksTo, onSelect }) {
  return (
    <section className="animate__animated animate__bounceIn font-mono text-center bg-amber-400 rounded-4xl shadow-xl shadow-black/40 h-150 mx-5 w-100 flex flex-col">
      {/* TITLE */}
      <h2 className="font-bold text-2xl mt-15 shrink-0">{title}</h2>

      {/* BUTTON AREA */}
      <div className="flex-1 flex items-center justify-center">
        <div className="grid grid-cols-3 auto-rows-fr gap-4 w-full px-6 place-items-stretch">
          {(linksTo ?? []).map((text, index) => (
            <button
              key={index}
              onClick={() => onSelect(text)} // ✅ send to parent
              className="
                text-xl w-full h-full aspect-square border cursor-pointer rounded-sm
                transition-transform duration-200 ease-out overflow-hidden
                hover:-translate-x-1 hover:translate-y-1
                active:-translate-x-2.5 active:translate-y-2.5
                hover:bg-black hover:text-amber-400
                hover:shadow-[10px_-10px_0_rgba(255,126,0,0.9)]
                active:shadow-[15px_-15px_0_rgba(255,80,0,0.7)]
              "
            >
              {text}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
