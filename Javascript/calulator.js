function calculate(a, b, op) {
    switch(op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return b !== 0 ? a / b : 'Undefined';
        default: return 'Invalid';
    }
}

let a = parseFloat(prompt("Enter first number:"));
let b = parseFloat(prompt("Enter second number:"));
let op = prompt("Enter operation (+ - * /):");

alert("Result: " + calculate(a, b, op));
