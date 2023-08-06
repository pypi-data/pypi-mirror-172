import uvicorn as uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import const

#here we just set the N is 50,it could be 500,5000 or whatever 
#the geometric_series_sum could be evaluated quickly.
const.N=50

app = FastAPI()

# - Find and fix the errors in the following program
# - Refactor the program to make it more modular (using a Pythonic style, e.g. numpy)
# - Implement an additional function geometric_series_sum() which takes an input parameter a and r
#   to calculate the sum of the first N elements of: a + a*r + a*r^2 + a*r^3 + ...
# - Test the application (what approach would you use for test?)


class Msg(BaseModel):
	msg: str


class GenerateData(BaseModel):
	a: int
	r: int


@app.post("/isGeometricSeries")
async def is_geometric_series_post(inp: Msg):
        
	result=False
	
	try:
		values_list = inp.msg.split(",")
		values_int_list=[int(i) for i in values_list]
		
		result = check_if_geometric_series(values_int_list)
	except ValueError:
		pass
	except:
		pass
	return {"The input sequence is geometric": result}
        

@app.post("/geometricSeriesSum")
async def geometric_series_sum(inp: GenerateData):
	try:
		if inp.r != 0:
			sum = geometric_sum(inp.a,inp.r)
			return {"The sum of geometric series is":sum}
		else:
			return {"The r cannot be zero":inp.r}
	except Exception as err:
		return {"The server internal error":err}

#the formula for the sum of geometric series is following:
#sum=a*(1-r^N)/(1-r) when r!=1  or
#sum=Na when r=1
def geometric_sum(a:int,r:int) -> int:
	return const.N * a if r==1 else a * (1-exponent(r,const.N))/(1-r)

#base parameter: power base,e.g. 2 in 2^3.
#exp parameter : the exponent of base, e.g. 3 in 2^3
#the algorithm here is binary multiplication,a quick way to get the value.
def exponent(base,exp) ->int:
	result = 0;

	if   exp % 2==1:
		result = base * exponent(base,exp-1);
	elif exp == 0:
		result = 1;
	elif exp == 2:
		result = base*base;
	else:
		half = exponent(base, exp / 2);
		result = half * half;

	return result;

def check_if_geometric_series(series: list) -> bool:
	"""
	Example:
	check_if_geometric_series([3, 6, 12, 24])
	True
	check_if_geometric_series([1, 2, 3, 4])
	False
	"""
	try:
		common_ratio = series[1] / series[0]
		for index in range(len(series) - 1):
			if series[index + 1] / series[index] != common_ratio:
				return False
	except ZeroDivisionError:
		return False
	else:
		return True   
        

if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8001)
