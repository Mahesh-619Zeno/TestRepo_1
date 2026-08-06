function isPalindrome(str) {
    return str === str.split('').reverse().join('');
}

let str = prompt("Enter a string:");
alert(isPalindrome(str) ? "Palindrome" : "Not a palindrome");
