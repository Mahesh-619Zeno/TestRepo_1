// todo.js
const fs = require('fs');

let todos = [];

function loadTodos() {
    try {
        const data = fs.readFileSync('todos.json');
        todos = JSON.parse(data);
    } catch {
        todos = [];
    }
}

function saveTodos() {
    fs.writeFileSync('todos.json', JSON.stringify(todos, null, 4));
}

function addTodo(title) {
    todos.push({ title, completed: false });
    saveTodos();
    console.log("Todo added!");
}

function listTodos() {
    console.log("\nYour Todos:");
    todos.forEach((todo, i) => {
        console.log(`${i + 1}. [${todo.completed ? 'x' : ' '}] ${todo.title}`);
    });
}

function toggleTodo(index) {
    if (todos[index]) {
        todos[index].completed = !todos[index].completed;
        saveTodos();
        console.log("Toggled!");
    } else {
        console.log("Invalid index");
    }
}

function deleteTodo(index) {
    if (todos[index]) {
        todos.splice(index, 1);
        saveTodos();
        console.log("Deleted!");
    } else {
        console.log("Invalid index");
    }
}

function showMenu() {
    console.log(`
--- TODO MENU ---
1. Add Todo
2. List Todos
3. Toggle Todo
4. Delete Todo
5. Exit
`);
}

function main() {
    loadTodos();
    const readline = require('readline-sync');
    while (true) {
        showMenu();
        const choice = readline.question("Choose an option: ");
        if (choice === '1') {
            const title = readline.question("Enter todo title: ");
            addTodo(title);
        } else if (choice === '2') {
            listTodos();
        } else if (choice === '3') {
            const index = parseInt(readline.question("Enter index to toggle: ")) - 1;
            toggleTodo(index);
        } else if (choice === '4') {
            const index = parseInt(readline.question("Enter index to delete: ")) - 1;
            deleteTodo(index);
        } else if (choice === '5') {
            break;
        } else {
            console.log("Invalid choice!");
        }
    }
}

main();
