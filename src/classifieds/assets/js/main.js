String.prototype.ucwords = function() {
    return (this + '').replace(/^([a-z])|\s+([a-z])/g, function ($1) {
      return $1.toUpperCase();
  });
}
String.prototype.preety = function() {
    return (this + '').replace(/(\_|\-)/g,' ');
}