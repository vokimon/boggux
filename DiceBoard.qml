import QtQuick 2.3
import QtQuick.Layouts 1.0

Item {
	id: diceBox
	property int boxSize: {
		var w = width
		if (height < w)
			w = height
		return w
	}
	property bool tracking: false
	property color diceColor: '#eea'
	property int diceGap: boxSize/80
	property int diceSize: (boxSize-diceGap*3)/4
//	property var game: 'ABDCEFGHIJKLLMNNÑOPQRSSTUVWXYZAAAEEEIIIOOOUUURRRSSSSSDDLL'
	property var game: 'HERINSDAMEPCESFIHEUOETNKZVNDAEVITEGNTAOAEIRCALESSIRMOAGENLUYJAMQOBWILRUESEONTDXORFIABATRILLUSPET'

	property var path: []

	signal wordCompleted(string word)

	function endWord()
	{
		var intendedWord = path.map(function(index) { return game[index] }).join('')
		this.wordCompleted(intendedWord)
	}

	function adjacent(first, second)
	{
		if (second < first) return adjacent(second, first)
		var diff = second - first
		if (diff == 1) return first%4 != 3
		if (diff == 5) return first%4 != 3
		if (diff == 3) return first%4 != 0
		return diff == 4
	}

	function addPath(dice) {
		var pos = path.indexOf(dice.i)
		if (pos != -1) {
			path = path.slice(0,pos+1)
			return
		}
		var last = path.slice(-1)[0]
		if (path.length && ! adjacent(dice.i, path.slice(-1)[0])) return
		path.push(dice.i)
		path = path
	}

	Rectangle {

		color: "#453"
		x: parent.width/2 - parent.boxSize/2
		y: parent.height/2 - parent.boxSize/2


		Grid {
			width: height
			columns: 4
			layoutDirection: Grid.LeftToRight
			spacing: diceBox.diceGap

			Repeater {
				id: dices
				model: 16
				Rectangle {
					id: dice
					property int i: index
					property string letter: diceBox.game[index]
					property int row : Math.floor(index / 4)
					property int col : index % 4
					color: diceBox.diceColor
					width: diceBox.diceSize
					height: width
					radius: width/8
					gradient: Gradient {
						GradientStop { position: 0.0; color: Qt.darker(diceBox.diceColor) }
						GradientStop { position: 0.2; color: diceBox.diceColor }
						GradientStop { position: 0.8; color: diceBox.diceColor }
						GradientStop { position: 1.0; color: Qt.darker(diceBox.diceColor) }
					}

					clip: true
					Rectangle {
						id: face
						color: mouse.containsMouse ? '#eed': '#ddc'
						width: parent.width
						height: parent.width
						radius: width/2-width/8
						clip: true
						MouseArea {
							// Smaller to enable diagonal paths
							id: mouse
							property var activeArea: 0.7 * parent.width
							property var margin: (parent.width-activeArea)/2
							width: activeArea
							height: activeArea
							x: margin
							y: margin
							hoverEnabled: true
							acceptedButtons: Qt.AllButtons
							cursorShape: Qt.PointingHandCursor
							onPressed: {
								if (diceBox.tracking) {
									diceBox.endWord()
									diceBox.tracking = false
									diceBox.path=[]
								}
								else {
									diceBox.tracking = true
									diceBox.path=[]
									diceBox.addPath(dice)
								}
							}
							onEntered:  {
								if (!diceBox.tracking) return
								diceBox.addPath(dice)
							}
						}
					}
					Text {
						id: diceLetter
						anchors.fill: parent
						style: Text.Sunken
						styleColor: '#777'
						font.pixelSize: parent.height*.8
						verticalAlignment: Text.AlignVCenter
						horizontalAlignment: Text.AlignHCenter
						text: letter
					}
				}
			}
		}
		Repeater {
			model: diceBox.path
			Rectangle {
				property var dotSize: diceBox.diceSize/3
				property var row : Math.floor(modelData/4)
				property var col : modelData%4
				function center(n) {
					return n*(diceBox.diceSize+diceBox.diceGap) +
						diceBox.diceSize/2 - dotSize/2
					}
				x: center(col)
				y: center(row)
				width: dotSize
				height: dotSize
				radius: dotSize/2
				color: 'blue'
				opacity: 0.5
			}
		}
		Repeater {
			model: diceBox.path.slice(0,-1)

			Line {
				opacity: 0.2
				color: 'blue'
				property var dotSize: diceBox.diceSize/5
				height: dotSize
				radius: dotSize/2
				property var next : diceBox.path[index+1>=diceBox.path.length ? index : index+1]
				function center(n) {
					return n*(diceBox.diceSize+diceBox.diceGap) +
						diceBox.diceSize/2 - dotSize/2
					}
				x1: center(modelData%4) + dotSize/2
				y1: center(Math.floor(modelData/4))
				x2: center(next%4) + dotSize/2
				y2: center(Math.floor(next/4))
			}
		}

	}
}
