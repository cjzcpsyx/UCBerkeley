var ex1 = function() {
	var setMessage;
	var getMessage;
	(function() {
		var message = "initial message";
		setMessage = function(x) {message = x;};
		getMessage = function() {return message;};
	})();
	console.log(getMessage());
	setMessage("meet me by the docks at midnight");
	console.log(getMessage());
};
var ex2 = function() {
	var a = "This string is so cool.";
	var cooler = function() {
		var a = "This string is even cooler.";
		coolest();
		console.log(a);
	};
	var coolest = function() {
		a = "This string is the coolest!";
	};
	cooler();
	console.log(a);
};
var ex3 = function() {
	var array = ["c", "a", "l"];
	var lambdas = [];
	for (var index in array) {
		lambdas.push(function() {return array[index];});
	};
	console.log(lambdas[0]());
	console.log(lambdas[1]());
	console.log(lambdas[2]());
}