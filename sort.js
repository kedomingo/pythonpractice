// https://www.codewars.com/kata/a-string-of-sorts/train/javascript
function sortString(string, ordering) {
  ordering = ordering.split('').reverse()
  order = {}
  for (var i in ordering) {
    order[ordering[i]] = i
  }
  return string.split('').sort(function(x, y){
    var x = (typeof order[x] == 'undefined') ? -99999 : order[x];
    var y = (typeof order[y] == 'undefined') ? -99999 : order[y];
    return y-x;
  }).join('');
}

x = sortString("banana","an");
console.log(x)
