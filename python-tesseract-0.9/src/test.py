import jfunc as j
puts=j.puts


puts("Warining Level is %s"%8,8)
puts("Warining Level is %s"%11,11)
puts(1.21,3,"apple",[1,2,3],{1:1,2:2},192)
puts(1.21,3,"apple",[1,2,3],192,END=",")
puts(1.21,3,"apple",[1,2,3],192,END=" ")
puts(1.21,3,"apple",[1,2,3],192,START="*"*10,END="%s,\n"%("^"*10))




