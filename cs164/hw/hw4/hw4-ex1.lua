function fibCo(a, b)
	coroutine.yield(a)
	fibCo(b, a+b)
end

function fib()
	return coroutine.wrap(function() fibCo(0, 1) end)
end

function takeCo(stream, n)
	if n > 1 then
		coroutine.yield(stream())
		takeCo(stream, n-1)
	else
		coroutine.yield(stream())
	end
end

function take(stream, n)
	return coroutine.wrap(function() takeCo(stream,n) end)
end

function filterCo(stream, prop)
	temp = stream()
	while not prop(temp) do
		temp = stream()
	end
	coroutine.yield(temp)
	filterCo(stream, prop)
end

function filter(stream, prop)
	return coroutine.wrap(function() filterCo(stream,prop) end)
end

function mapCo(stream, f)
	coroutine.yield(f(stream()))
	mapCo(stream, f)
end

function map(stream, f)
	return coroutine.wrap(function() mapCo(stream, f) end)
end

fibStream = fib()

isEven = function(x) return x % 2 == 0 end
evenFib = filter(fibStream, isEven)

plusOne = function(x) return x+1 end
evenFibPlusOne = map(evenFib, plusOne)

for i in take(evenFibPlusOne, 5) do
	print(i)
end