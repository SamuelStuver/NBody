from pyinstrument import Profiler

profiler = Profiler()

profiler.start()
for i in range(100):
    print()

profiler.stop()
print(profiler.output_text(unicode=True, color=True))