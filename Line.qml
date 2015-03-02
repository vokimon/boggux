import QtQuick 2.3
 
Rectangle {
    id: l
    property alias x1: l.x
    property alias y1: l.y
 
    property real x2: l.x
    property real y2: l.y
 
    color: "black"
    height: 2
    smooth: true;
 
    transformOrigin: Item.Left;
 
    width: getWidth(x1,y1,x2,y2);
    rotation: getSlope(x1,y1,x2,y2);
 
    function getWidth(sx1,sy1,sx2,sy2)
    {
		var dx=sx2-sx1
		dx*=dx
		var dy=sy2-sy1
		dy*=dy
        return Math.sqrt(dx+dy);
    }
 
    function getSlope(sx1,sy1,sx2,sy2)
    {
		var dx=sx2-sx1
		var dy=sy2-sy1
		var angle  = Math.atan2(dy, dx) * 180 / Math.PI
		return angle
    }
}
