# Run this script to start the bots for Utrecht and Vleuten

echo "Starting bots..."

python3 -m app.bot Utrecht &
if [[ "$?" != "0" ]]; then
	echo "Error with Utrecht bot, aborting..."
	exit 1
fi

python3 -m app.bot Vleuten &
if [[ "$?" != "0" ]]; then
	echo "Error with Vleuten bot, aborting..."
	exit 1
fi

echo "Bots are running..."