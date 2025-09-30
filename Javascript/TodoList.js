// todo.js
const fs = require('fs');

let Todos = [];

function load_todos() {
    try {
        const data = fs.readFileSync('todos.json');
        Todos = JSON.parse(data);
    } catch {
        Todos = [];
    }
}

function save_todos() {
    fs.writeFileSync('todos.json', JSON.stringify(Todos, null, 4));
}

function ADD_TODO(title_of_todo) {
    Todos.push({ title: title_of_todo, completed: false });
    save_todos();
    console.log("Todo added!");
}

function listTodos() {
    console.log("\nYour Todos:");
    Todos.forEach((t, i) => {
        console.log(`${i + 1}. [${t.completed ? 'x' : ' '}] ${t.title}`);
    });
}

function toggleTodo(INDEX) {
    if (Todos[INDEX]) {
        Todos[INDEX].completed = !Todos[INDEX].completed;
        save_todos();
        console.log("Toggled!");
    } else {
        console.log("Invalid index");
    }
}

function deleteTodo(index_to_delete) {
    if (Todos[index_to_delete]) {
        Todos.splice(index_to_delete, 1);
        save_todos();
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
    load_todos();
    const readline = require('readline-sync');
    while (true) {
        showMenu();
        const choice = readline.question("Choose an option: ");
        if (choice === '1') {
            const title = readline.question("Enter todo title: ");
            ADD_TODO(title);
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