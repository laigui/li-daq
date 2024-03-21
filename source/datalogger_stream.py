# Liquid Instrument Datalogger streaming
#
# This example demonstrates use of the Datalogger instrument to
# stream time-series voltage data and plot it using matplotlib.
#
import matplotlib.pyplot as plt

from moku.instruments import Datalogger

# Connect the instrument
i = Datalogger('[fe80::7269:79ff:feb0:a1c%10]', force_connect=True)
   
try:
    # Set the sample rate from 10 to 10e6 Hz
    i.set_samplerate(10e3)

    # Set the duration time of data stream in seconds
    i.start_streaming(10)

    # Set up the plotting parameters
    plt.ion()
    fig, ax = plt.subplots()
    plt.grid(visible=True)
    plt.ylim([-1, 1])

    line1, = plt.plot([])

    # This loops continuously updates the plot with new data
    while True:
        # get the chunk of streamed data
        data = i.get_stream_data()
        if data:
            # Print out the data
            #print(data['time'], data['ch1'], data['ch2'], data['ch3'], data['ch4'])
            plt.xlim([data['time'][0], data['time'][-1]])
            # Update the plot
            line1.set_ydata(data['ch1'])
            line1.set_xdata(data['time'])
            fig.canvas.draw()
            plt.pause(0.1) # Wait for a while before the next update

except Exception as e:
    i.stop_streaming()
    print(e)
finally:
    i.relinquish_ownership()