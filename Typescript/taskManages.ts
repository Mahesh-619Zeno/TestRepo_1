// taskManager.ts

type TaskStatus = "pending" | "in-progress" | "completed" | "archived";

interface Task {
  id: number;
  title: string;
  description?: string;
  dueDate?: Date;
  status: TaskStatus;
  createdAt: Date;
  updatedAt: Date;
}

interface FilterOptions {
  status?: TaskStatus;
  dueBefore?: Date;
  dueAfter?: Date;
  searchKeyword?: string;
}

interface SortOptions {
  sortBy: "title" | "dueDate" | "createdAt" | "updatedAt";
  order: "asc" | "desc";
}

class TaskManager {
  private tasks: Task[] = [];
  private idCounter = 1;

  addTask(title: string, description?: string, dueDate?: Date): Task {
    const now = new Date();
    const task: Task = {
      id: this.idCounter++,
      title,
      description,
      dueDate,
      status: "pending",
      createdAt: now,
      updatedAt: now,
    };
    this.tasks.push(task);
    return task;
  }

  getTaskById(id: number): Task | undefined {
    return this.tasks.find(task => task.id === id);
  }

  updateTask(id: number, updates: Partial<Omit<Task, "id" | "createdAt">>): Task | null {
    const task = this.getTaskById(id);
    if (!task) return null;

    Object.assign(task, updates);
    task.updatedAt = new Date();
    return task;
  }

  deleteTask(id: number): boolean {
    const index = this.tasks.findIndex(task => task.id === id);
    if (index !== -1) {
      this.tasks.splice(index, 1);
      return true;
    }
    return false;
  }

  filterTasks(filters: FilterOptions): Task[] {
    return this.tasks.filter(task => {
      const matchStatus = filters.status ? task.status === filters.status : true;
      const matchDueBefore = filters.dueBefore ? task.dueDate && task.dueDate < filters.dueBefore : true;
      const matchDueAfter = filters.dueAfter ? task.dueDate && task.dueDate > filters.dueAfter : true;
      const matchKeyword = filters.searchKeyword
        ? task.title.includes(filters.searchKeyword) || task.description?.includes(filters.searchKeyword)
        : true;
      return matchStatus && matchDueBefore && matchDueAfter && matchKeyword;
    });
  }

  sortTasks(tasks: Task[], options: SortOptions): Task[] {
    const sorted = [...tasks];
    const { sortBy, order } = options;

    sorted.sort((a, b) => {
      let valA: string | number | Date = a[sortBy];
      let valB: string | number | Date = b[sortBy];

      if (valA instanceof Date && valB instanceof Date) {
        return order === "asc" ? valA.getTime() - valB.getTime() : valB.getTime() - valA.getTime();
      }

      if (typeof valA === "string" && typeof valB === "string") {
        return order === "asc" ? valA.localeCompare(valB) : valB.localeCompare(valA);
      }

      return 0;
    });

    return sorted;
  }

  listAllTasks(): Task[] {
    return this.tasks;
  }

  archiveCompletedTasks(): void {
    this.tasks.forEach(task => {
      if (task.status === "completed") {
        task.status = "archived";
        task.updatedAt = new Date();
      }
    });
  }

  clearArchivedTasks(): void {
    this.tasks = this.tasks.filter(task => task.status !== "archived");
  }

  printTasks(tasks: Task[] = this.tasks): void {
    console.log("Tasks:");
    tasks.forEach(task => {
      console.log(`- [${task.status.toUpperCase()}] (${task.id}) ${task.title} (Due: ${task.dueDate?.toDateString() || "N/A"})`);
    });
  }
}

// Example usage:

const manager = new TaskManager();

manager.addTask("Learn TypeScript", "Watch a tutorial", new Date("2025-08-15"));
manager.addTask("Write blog post", "Topic: TypeScript vs JavaScript");
manager.addTask("Submit project", undefined, new Date("2025-08-20"));

manager.updateTask(2, { status: "in-progress" });

const filtered = manager.filterTasks({ status: "pending" });
const sorted = manager.sortTasks(filtered, { sortBy: "dueDate", order: "asc" });

manager.printTasks(sorted);

manager.archiveCompletedTasks();
manager.clearArchivedTasks();
