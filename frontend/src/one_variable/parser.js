function tokenize(input) {
  let i = 0;

  const isDigit = c => /[0-9]/.test(c);
  const isLetter = c => /[a-zA-Z]/.test(c);
  const isAlphaNum = c => /[a-zA-Z0-9]/.test(c);

  function skipWhitespace() {
    while (i < input.length && /\s/.test(input[i])) i++;
  }

  function readNumber() {
    let num = "";

    while (i < input.length && isDigit(input[i])) {
      num += input[i++];
    }

    if (input[i] === ".") {
      num += input[i++];
      while (i < input.length && isDigit(input[i])) {
        num += input[i++];
      }
    }

    return { type: "number", value: parseFloat(num) };
  }

  function readIdentifier() {
    let id = "";

    if (!isLetter(input[i])) {
      throw new Error("Invalid identifier start");
    }

    id += input[i++];

    while (i < input.length && isAlphaNum(input[i])) {
      id += input[i++];
    }

    return { type: "identifier", value: id };
  }

  function nextToken() {
    skipWhitespace();

    if (i >= input.length) return { type: "eof" };

    const ch = input[i];

    if (isDigit(ch)) return readNumber();
    if (isLetter(ch)) return readIdentifier();

    i++;

    if ("+-*/^()".includes(ch)) {
      return { type: ch };
    }

    throw new Error("Unexpected character: " + ch);
  }

  return { nextToken };
}

export default function parse(input) {
  const lexer = tokenize(input);
  let current = lexer.nextToken();

  const FUNCTIONS = new Set(["sin", "cos", "tan", "log10", "ln"]);

  const eat = (type) => {
    if (current.type === type) {
      current = lexer.nextToken();
    } else {
      throw new Error(`Expected ${type}, got ${current.type}`);
    }
  };

  const parseExpr = () => {
    let node = parseTerm();

    while (current.type === "+" || current.type === "-") {
      const op = current.type;
      eat(op);
      node = { type: "binary", op, left: node, right: parseTerm() };
    }

    return node;
  };

  const parseTerm = () => {
    let node = parsePower();

    while (current.type === "*" || current.type === "/") {
      const op = current.type;
      eat(op);
      node = { type: "binary", op, left: node, right: parsePower() };
    }

    return node;
  };

  const parsePower = () => {
    let node = parseUnary();

    while (current.type === "^") {
      eat("^");
      node = { type: "binary", op: "^", left: node, right: parseUnary() };
    }

    return node;
  };

  const parseUnary = () => {
    if (current.type === "-") {
      eat("-");
      return { type: "unary", op: "-", value: parseUnary() };
    }
    return parsePrimary();
  };

  const parsePrimary = () => {
    const token = current;

    if (token.type === "number") {
      eat("number");
      return { type: "number", value: token.value };
    }

    if (token.type === "identifier") {
      const name = token.value;

      if (name === "pi" || name === "e") {
        eat("identifier");
        return { type: "constant", value: name };
      }

      if (name === "x") {
        eat("identifier");
        return { type: "variable", name };
      }

      if (FUNCTIONS.has(name)) {
        eat("identifier");

        if (current.type !== "(") {
          throw new Error("Expected '(' after function: " + name);
        }

        eat("(");
        const arg = parseExpr();
        eat(")");

        return { type: "call", name, arg };
      }

      throw new Error("Unknown identifier: " + name);
    }

    if (token.type === "(") {
      eat("(");
      const node = parseExpr();
      eat(")");
      return node;
    }

    throw new Error("Unexpected token: " + token.type);
  };

  const ast = parseExpr();

  if (current.type !== "eof") {
    throw new Error("Unexpected input after expression");
  }

  return ast;
}