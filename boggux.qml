import QtQuick 2.3
import QtQuick.Layouts 1.1
import QtQuick.Window 2.2
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2
import QtQuick.Dialogs 1.2

Window {
	id: main
	property var words : []
	property string dices : 'XXXXXXXXXXXXXXXX'

	function setGame(game)
	{
		dices=game
		words=[]
		lastWordMessage.reset()
	}
	function badWord(word, message)
	{
		lastWordMessage.error(word,message)
	}

	function totalPoints()
	{
		return words.reduce(function(sum,value){return sum+wordPoints(value)},0)
	}
	function wordPoints(word)
	{
		var points = word.length - 2
		return (points < 0) ? 0 : points
	}
	function wordCompleted(word)
	{
		words.splice(0,0,word)
		var points = wordPoints(word)
		lastWordMessage.success(word,(
			points == 1 ?
			qsTr("¡%1 punto!"):
			qsTr("¡%1 puntos!")
				).arg(wordPoints(word)))
		words=main.words
	}
	function validateWord(word)
	{
		if (word.length<3)
			return qsTr("Tiene menos de 3 letras")
		if (words.indexOf(word) != -1)
			return qsTr("Repetida")
		return false
	}

	title: qsTr("BoGGuX")
	color: '#564'
	width: Screen.width/2
	height: Screen.height/2

	Action {
		id: shuffleAction
		text: qsTr("Remena")
		onTriggered: { gameEngine.shuffle() }
	}

	GridLayout {
		anchors.fill: parent
		Layout.alignment: Qt.AlignHCenter
		Layout.fillWidth: true
		columns: 1
		flow: GridLayout.LeftToRight

		Rectangle {
			id: title
			Layout.alignment: Layout.Center
			Layout.columnSpan: parent.columns
			color: "#494"
			radius: 10
			width: childrenRect.width+radius*4
			height: childrenRect.height+radius*2
			Text {
				x: parent.radius*2
				y: parent.radius
				text: "BoGGuX"
				color: '#eef'
				font.bold: true
				font.pixelSize: parent.radius*2.2
			}
		}
		RowLayout {
			id: buttons
			Layout.maximumWidth: parent.width
			Layout.alignment: Layout.Center
			Layout.fillWidth: true
			Button {
				Layout.alignment: Layout.Center
				action: shuffleAction
			}
			Button {
				Layout.alignment: Layout.Center
				text: qsTr("Configura")
			}
		}
		Item {
			id: diceBoardContainer
			Layout.minimumWidth: 200
			Layout.minimumHeight: 200
			Layout.maximumWidth: parent.width
			Layout.fillWidth: true
			Layout.fillHeight: true
			Layout.alignment: Layout.Top | Layout.Center
			DiceBoard {
				id: diceBoard
				game: main.dices
				anchors.fill: parent
				onWordCompleted: {
					gameEngine.wordCompleted(word)
				}
			}
		}
		Text {
			id: lastWordMessage
			Layout.alignment: Qt.AlignHCenter
			Layout.fillWidth: true
			horizontalAlignment: Text.AlignHCenter
			width: childrenRect.width
			height: childrenRect.height
			text: qsTr('')
			font.bold: true
			function reset()
			{
				text='Click, drag and click to end the word'
				color='#5a5'
			}
			function set(color, word, message)
			{
				this.color = color
				this.text = "%1:  %2".arg(word).arg(message)
			}
			function error(word, message)
			{
				set('#f88', word, message)
			}
			function success(word, message)
			{
				set('#5e5', word, message)
			}
		}
		Label {
			id: headerText
			Layout.alignment: Layout.Center
			Layout.maximumWidth: parent.width
			horizontalAlignment: Text.AlignHCenter
			color: 'white'
			font.bold: true
			smooth: true
			text: (qsTr("Puntos: %1   Palabras: %2")
				.arg(main.totalPoints())
				.arg(main.words.length)
				)
		}
		ListView {
			id: wordlist
			Layout.maximumWidth: parent.width
			Layout.minimumHeight: 200
			Layout.minimumWidth: 250
			Layout.alignment: Qt.AlignHCenter
			Layout.fillHeight: false
			Layout.rowSpan: 2
			clip: true
			model: main.words
			delegate:
				Rectangle {
					width: parent.width
					height: word.height
					color: '#8a7'
					Text {
						id: word
						text: qsTr('%1 (%2)')
							.arg(main.words[index])
							.arg(wordPoints(main.words[index]))
					}
					ColorAnimation on color {
						to: 'orange'; duration: 1000
					}
				}
			add: Transition {
				NumberAnimation { properties: "x,y"; from: 100; duration: 1000 }
			}
		}
	}
	function onLoad()
	{
		shuffle()
	}
}
