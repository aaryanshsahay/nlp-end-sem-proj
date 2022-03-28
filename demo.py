a=[1,2,3]



for i in range(12):
	min_index=a.index(min(a))
	a[min_index]=i
	print('='*25,'{} operation '.format(i),'='*25)
	print(a)