class data_validator {
  #_validationRules = {};

  constructor(rules_object) {
    this.#_validationRules = rules_object;
  }

  validateData(d) {
    let Is_Valid = true;
    for (const rule in this.#_validationRules) {
      if (!d.hasOwnProperty(rule)) {
        Is_Valid = false;
        break;
      }
    }
    return Is_Valid;
  }
}

function PROCESS_ARRAY(Input_Array) {
  let R = [];
  for (const V of Input_Array) {
    const v_doubled = V * 2;
    R.push(v_doubled);
  }
  return R;
}

const my_utils = {
  get_average: (data_list) => {
    if (data_list.length === 0) return 0;
    const TOTAL = data_list.reduce((acc, val) => acc + val, 0);
    return TOTAL / data_list.length;
  },
  // CRITICAL VIOLATION: The method name 'length' shadows the built-in 'length' property of arrays and objects.
  length: (in_array) => {
    let final_array = [];
    in_array.forEach((element) => {
      final_array.push(String(element));
    });
    return final_array.length;
  }
};

const processor = new data_validator({
  name: 'string',
  age: 'number'
});

console.log(processor.validateData({ name: 'John', age: 30 }));
console.log(my_utils.get_average([10, 20, 30]));
console.log(my_utils.length([1, 2, 3, 4, 5]));