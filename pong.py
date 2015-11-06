WINDOWWIDTH = 32
WINDOWHEIGHT = 32
LINETHICKNESS = 2
PADDLESIZE = 5
PADDLEOFFSET = 1

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (0,255,255)



#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
	if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
		ballDirY = ballDirY * -1.0
	if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
		ballDirX = ballDirX * -1.0
	return ballDirX, ballDirY

#Checks is the ball has hit a paddle, and 'bounces' ball off it.     
def checkHitBall(ball, paddle1, paddle2, ballDirX):
	if ballDirX < 0 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
		return -1.01#more speed!
	elif ballDirX > 0 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
		return -1.01
	else: return 1

#Checks to see if a point has been scored returns new score
def checkPointScored(paddle1, ball, score, ballDirX):
	#reset points if left wall is hit
	if ball.left == LINETHICKNESS: 
		return 0
	#1 point for hitting the ball NO!
	elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
		score += 0
		return score
	#5 points for beating the other paddle
	elif ball.right == WINDOWWIDTH - LINETHICKNESS:
		score += 1
		return score
	#if no points scored, return score unchanged
	else: return score

#Artificial Intelligence of computer player 
def artificialIntelligence2(ball, ballDirX, paddle2):
	#If ball is moving away from paddle, center bat
	if ballDirX < 0:
		if paddle2.centery < (WINDOWHEIGHT/2):
			paddle2.y += 1
		elif paddle2.centery > (WINDOWHEIGHT/2):
			paddle2.y -= 1
	#if ball moving towards bat, track its movement. 
	elif ballDirX >0:
		if paddle2.centery < ball.centery:
			paddle2.y += 1
		else:
			paddle2.y -=1
	return paddle2

def artificialIntelligence1(ball, ballDirX, paddle1):
	#If ball is moving away from paddle, center bat???
	if ballDirX < 0:
		if paddle1.centery < ball.centery:
			paddle1.y += 1
		else:
			paddle1.y -=1
	#if ball moving towards bat, track its movement. ???
	elif ballDirX > 0:
		if paddle1.centery < (WINDOWHEIGHT/2):
			paddle1.y += 1
		elif paddle1.centery > (WINDOWHEIGHT/2):
			paddle1.y -= 1
	return paddle1