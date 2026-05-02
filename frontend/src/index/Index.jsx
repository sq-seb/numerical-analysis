import { useRef, useState, useEffect } from "react";

import "animate.css";
import "./index.css";

import Card from "./Card";
import Marquee from "react-fast-marquee";
import { RiArrowGoBackLine } from "react-icons/ri";

const SafeMarquee = Marquee.default ?? Marquee;

// One variable
import Bisection from "../one_variable/Bisection";
import FalsePosition from "../one_variable/FalsePosition";
import NewtonRaphson from "../one_variable/NewtonRaphson";
import Secant from "../one_variable/Secant";
import MultipleRoots from "../one_variable/MultipleRoots";

// Systems of equations
import Jacobi from "../multiple_variables/Jacobi";
import GaussSeidel from "../multiple_variables/GaussSeidel";
import Sor from "../multiple_variables/Sor";

// Interpolation
import Vandermonde from "../interpolation/Vandermonde";
import Newton from "../interpolation/Newton";
import Lagrange from "../interpolation/Lagrange";
import LinearSpline from "../interpolation/LinearSpline";
import QuadraticSpline from "../interpolation/QuadraticSpline";
import CubicSpline from "../interpolation/CubicSpline";

// ===============================================================
export default function Index() {
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState(null);

  // Titles
  const title1 = "Solving equations of one variable";
  const title2 = "Solution of systems of equations";
  const title3 = "Interpolation";

  // Links
  const linksTo1 = [
    "Bisection",
    "False position",
    "Fixed point",
    "Newton-Raphson",
    "Secant",
    "Multiple roots",
  ];

  const linksTo2 = ["Jacobi", "Gauss-Seidel", "SOR"];

  const linksTo3 = [
    "Vandermonde",
    "Newton",
    "Lagrange",
    "Linear Spline",
    "Quadratic Spline",
    "Cubic Spline",
  ];

  const methodMap = {
    Bisection,
    "False position": FalsePosition,
    "Newton-Raphson": NewtonRaphson,
    Secant,
    "Multiple roots": MultipleRoots,

    Jacobi,
    "Gauss-Seidel": GaussSeidel,
    SOR: Sor,

    Vandermonde,
    Newton,
    Lagrange,
    "Linear Spline": LinearSpline,
    "Quadratic Spline": QuadraticSpline,
    "Cubic Spline": CubicSpline,
  };

  const SelectedComponent = selectedMethod ? methodMap[selectedMethod] : null;

  const currentLocation = selectedMethod
    ? `You're on ${selectedMethod}`
    : "";

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    audio.pause();
    audio.currentTime = 0;
  }, []);

  const toggleMusic = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }

    setIsPlaying(!isPlaying);
  };

  const goBack = () => setSelectedMethod(null);

  return (
    <div className="bg-yellow-200 h-screen w-screen">
      {/* HEADER */}
      <header className="flex flex-col gap-10 relative">
        <nav className="bg-amber-400 flex items-center h-15 m-0 shadow-xl">
          <div className="ml-8 animate__animated animate__flipInX">
            <a href="/">
              <img src="/favicon.svg" alt="Website logo" className="w-15" />
            </a>
          </div>

          <SafeMarquee
            gradient={true}
            gradientColor="oklch(82.8% 0.189 84.429)"
            gradientWidth={200}
            speed={200}
          >
            <div className="flex text-2xl font-mono gap-20 translate-x-200 items-center">
              <p className="font-bold text-5xl pr-300 overflow-hidden">NuMethods</p>

              <p className="font-bold">MADE BY</p>
              <p>Andrés Restrepo</p>
              <p>Juan Pablo Posso</p>
              <p className="pr-300">Sebastián Villegas</p>

              <p className="font-bold">PRESENTED TO</p>
              <p className="pr-300">Julián Rendón</p>
            </div>
          </SafeMarquee>
        </nav>

        {/* GO BACK + SPEECH BUBBLE */}
        {selectedMethod && (
          <div className="ml-8 fixed top-20 left-0 flex items-center gap-4 z-1">
            <button
              onClick={goBack}
              className="h-15 w-25 p-3 border rounded-full bg-amber-400 text-black hover:bg-black hover:text-amber-400 transition shadow-xl shadow-black/30 flex items-center justify-center cursor-pointer"
            >
              <RiArrowGoBackLine size={24} />
            </button>

            {/* speech bubble */}
            <div className="relative px-4 py-2 bg-black text-amber-400 font-mono shadow-lg rounded-2xl border border-amber-400/20 animate__animated animate__bounce animate-bounce">
              {currentLocation}

              {/* tail */}
              <div className="absolute -left-1.5 top-1/2 -translate-y-1/2 w-3 h-3 bg-black rotate-45 border-l border-b border-amber-400/20" />
            </div>
          </div>
        )}

        <audio ref={audioRef} src="music.mp3" loop />

        <div className="ml-auto mr-auto">
          <button
            onClick={toggleMusic}
            className={`w-45 text-3xl font-mono px-4 py-2 border rounded bg-amber-400 text-black hover:bg-black hover:text-amber-400 transition cursor-pointer shadow-xl shadow-black/30 ${
              isPlaying ? "animate__animated animate__flip animate-bounce" : ""
            }`}
          >
            {isPlaying ? ":) ⏸" : "Bored? ▶"}
          </button>
        </div>
      </header>

      {/* MAIN */}
      <main className="flex justify-around mt-10">
        {!selectedMethod ? (
          <>
            <Card
              title={title1}
              linksTo={linksTo1}
              onSelect={setSelectedMethod}
            />
            <Card
              title={title2}
              linksTo={linksTo2}
              onSelect={setSelectedMethod}
            />
            <Card
              title={title3}
              linksTo={linksTo3}
              onSelect={setSelectedMethod}
            />
          </>
        ) : (
          <div className="w-full flex justify-center">
            {SelectedComponent && <SelectedComponent />}
          </div>
        )}
      </main>
    </div>
  );
}