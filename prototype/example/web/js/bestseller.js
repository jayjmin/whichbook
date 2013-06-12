// Template
// Module Sayings & Class Greeter
// var Sayings;
// (function (Sayings) {
//     var Greeter = (function () {
//         function Greeter(message) {
//             this.greeting = message;
//         }
//         Greeter.prototype.greet = function () {
//             return "Hello, " + this.greeting;
//         };
//         return Greeter;
//     })();
//     Sayings.Greeter = Greeter;    
// })(Sayings || (Sayings = {}));

// var greeter = new Sayings.Greeter("world");
// var button = document.createElement('button');
// button.innerText = "Say Hello";
// button.onclick = function () {
//     alert(greeter.greet());
// };
// document.body.appendChild(button);


// Not Yet
var BestSellerList = (function () {
    function BestSellerList(message) {
        this.greeting = message;
    }
    BestSellerList.prototype.greet = function () {
        return "Hello, " + this.greeting;
    };
    return BestSellerList;
})();







//once the DOM is ready
$(document).ready(function(){
  // var binfoJson must be defined before.
  // Here, binfoJson is defined on the template html file
  // console.log(binfoJson[0].rank);
  // bsl = new BestSellerList({});
  // bsl.show();

  var options = {
    autoResize: true, // This will auto-update the layout when the browser window is resized.
    container: $('#main'), // Optional, used for some extra CSS styling
    offset: 2, // Optional, the distance between grid items
    itemWidth: 210 // Optional, the width of a grid item
  };

  // Get a reference to your grid items.
  var handler = $('#tiles li');

  // Call the layout function.
  handler.wookmark(options);



})
