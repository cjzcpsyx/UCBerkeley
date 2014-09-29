function makeIterator(array){
  var nextIndex = 0;
  return {
		next: function(){
			return nextIndex < array.length ?
				nextIndex++ :
				null;
		}
  }
}
var array = ["c", "a", "l"];
var lambdas = [];
var iter = makeIterator(array);
while ((x = iter.next()) != null) {
	var index = x;
	lambdas.push(function() {return array[index]});
}
console.log(lambdas[0]());
console.log(lambdas[1]());
console.log(lambdas[2]());