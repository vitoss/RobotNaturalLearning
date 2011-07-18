//
//  EchoClientViewController.m
//  EchoClient
//
//  Created by Muszu on 11-03-28.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

//#import "AsyncSocket.h" //tcpip
#import "AsyncUdpSocket.h"
#import "SocketClientIOSViewController.h"

#define FORMAT(format, ...) [NSString stringWithFormat:(format), ##__VA_ARGS__]

#define WELCOME_MSG  0
#define ECHO_MSG     1

#define MESSAGE_INTERVAL 0.5
#define MAX_ARM_SPEED 10

@implementation SocketClientIOSViewController
@synthesize logWindow, ipField, messageField, portField, listenSocket, connectedSockets;
@synthesize sendMsgButton, connectButton, accelerometer, acceptButton;


- (void)dealloc
{
    [super dealloc];
}

- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle


// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad
{
    [super viewDidLoad];
    
    listenSocket = [[AsyncUdpSocket alloc] initWithDelegate:self];
    connectedSockets = [[NSMutableArray alloc] initWithCapacity:1];
    
    isRunning = NO;
    
    messageField.delegate = self;
    portField.delegate = self;
    ipField.delegate = self;
    
    messageField.enabled = false;
    sendMsgButton.enabled = false;
    
    [listenSocket setRunLoopModes:[NSArray arrayWithObject:NSRunLoopCommonModes]];
    
    //acelerometer
    self.accelerometer = [UIAccelerometer sharedAccelerometer];
    self.accelerometer.updateInterval = MESSAGE_INTERVAL; //0.08
    self.accelerometer.delegate = self;
}


- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

-(IBAction) connectToServer: (id)sender {
    if( !isRunning ) {
        [self logMessage:@"Start connecting to server"];
        
        NSString *host = [ipField text];
        
        int port = [[portField text] intValue];
        
        if(port < 0 || port > 65535)
        {
            port = 0;
        }
        
        NSError *error = nil;
        AsyncUdpSocket *newHost = [[AsyncUdpSocket alloc] initWithDelegate:self];
        
        if(![newHost connectToHost:host onPort:port error:&error])
        {
            [self logMessage:FORMAT(@"Error starting client: %@", error)];
            return;
        } else {
            //enabling UI
            messageField.enabled = true;
            sendMsgButton.enabled = true;
            
            //chaning connect to disconect
            [connectButton setTitle:@"Disconnect" forState:UIControlStateNormal];
            
            ipField.enabled = false;
            portField.enabled = false;
            
            //
            isRunning = YES;
            [connectedSockets addObject:newHost];
            
        }
    } else {
        //[listenSocket disconnect]; //TCPIP
        [[connectedSockets lastObject] close]; //UDP - we assume only 1 connected socket for now
        
        //enabling UI
        ipField.enabled = NO;
        sendMsgButton.enabled = NO;
        messageField.enabled = NO;
        
        [connectButton setTitle:@"Connect" forState:UIControlStateNormal];
        
        isRunning = NO;
    }
    
}

//for listening
-(IBAction) acceptConnection: (id)sender {
    
    if( !isPortBinded ) {
        NSError *error = nil;
        
        //if( ![listenSocket bindToAddress:[ipField text] port:[[portField text] intValue] error:&error] ) {
        if( ![listenSocket bindToPort:[[portField text] intValue] error:&error] ) {
            [self logMessage:FORMAT(@"Error binding port: %@", error)];
            
            return;
        } else {
            [self logMessage:@"Port binded"];
            
            //chaning connect to disconect
            [acceptButton setTitle:@"Disconnect" forState:UIControlStateNormal];
            
            isPortBinded = YES;
            portField.enabled = false;
            
            [listenSocket receiveWithTimeout:-1 tag:ECHO_MSG];
        }
    } else {
        [listenSocket close];
        
        [acceptButton setTitle:@"Connect" forState:UIControlStateNormal];
        
        isPortBinded = NO;
    }
}

-(IBAction) sendMessage: (id) sender {
    [self logMessage:@"Start sending message to server"];
    NSMutableString *message = [NSMutableString stringWithString:[messageField text]];
    //[message appendString:@"\r\n"];
    [message appendString:@"\n"];
    NSData *messageData = [message dataUsingEncoding:NSUTF8StringEncoding];
    
    for(int i = 0; i < [connectedSockets count]; i++)
    {
        //sending only to connected hosts
        [[connectedSockets objectAtIndex:i] sendData:messageData withTimeout:-1 tag:ECHO_MSG];
    }

}

#pragma mark Socket Delegates - AsyncUdpSocket


- (void)onUdpSocket:(AsyncUdpSocket *)sock didSendDataWithTag:(long)tag {
    [self logMessage:@"Message sent"];
}

- (void)onUdpSocket:(AsyncUdpSocket *)sock didNotSendDataWithTag:(long)tag dueToError:(NSError *)error {
    [self logMessage:FORMAT(@"Message not sent: %@", error)];
}

- (BOOL)onUdpSocket:(AsyncUdpSocket *)sock didReceiveData:(NSData *)data withTag:(long)tag fromHost:(NSString *)host port:(UInt16)port {
    
    NSData *strData = [data subdataWithRange:NSMakeRange(0, [data length] - 2)];
	NSString *msg = [[[NSString alloc] initWithData:strData encoding:NSUTF8StringEncoding] autorelease];
	if(msg)
	{
		[self logMessage:msg];
	}
	else
	{
		[self logMessage:@"Error converting received data into UTF-8 String"];
	}

    [self logMessage:@"didReceiveData from host on port"];
    [listenSocket receiveWithTimeout:-1 tag:ECHO_MSG];
    return YES;
}

- (void)onUdpSocket:(AsyncUdpSocket *)sock didNotReceiveDataWithTag:(long)tag dueToError:(NSError *)error {
    [self logMessage:@"didNOTReceiveData"];
}


- (void)onUdpSocketDidClose:(AsyncUdpSocket *)sock
{
    [connectedSockets removeObject:sock];
    
    messageField.enabled = false;
    sendMsgButton.enabled = false;
    
    //chaning connect to disconect
    [connectButton setTitle:@"Connect" forState:UIControlStateNormal];
    
    ipField.enabled = true;
    portField.enabled = true;
    isRunning = NO;
    
}



#pragma mark - Acelerometer
- (void)accelerometer:(UIAccelerometer *)accelerometer didAccelerate:(UIAcceleration *)acceleration {
    
    if( isRunning ) {
        //[self logMessage:@"Send acceleration data."];
        
        float xSpeedFactor = acceleration.x;
        if( xSpeedFactor < 0 )
            xSpeedFactor = -xSpeedFactor;
        
        if( xSpeedFactor > 0.66 )
            xSpeedFactor = 1;
        else if( xSpeedFactor > 0.33 )
            xSpeedFactor = 0.5;
        else 
            xSpeedFactor = 0;
        
        float ySpeedFactor = acceleration.y;
        
        if( ySpeedFactor < 0 )
            ySpeedFactor = -ySpeedFactor;
        
        if( ySpeedFactor > 0.66  )
            ySpeedFactor = 1;
        else if( ySpeedFactor > 0.33  )
            ySpeedFactor = 0.5;
        else 
            ySpeedFactor = 0;
        
        
        float zSpeedFactor = acceleration.z;
        
        if( zSpeedFactor < 0 )
            zSpeedFactor = -zSpeedFactor;
        
        if( zSpeedFactor > 0.66 )
            zSpeedFactor = 1;
        else if( zSpeedFactor > 0.33 )
            zSpeedFactor = 0.5;
        else 
            zSpeedFactor = 0;
        
        //first axis
        float xAxis = MAX_ARM_SPEED*xSpeedFactor*MESSAGE_INTERVAL;
        float yAxis = MAX_ARM_SPEED*ySpeedFactor*MESSAGE_INTERVAL;
        float zAxis = MAX_ARM_SPEED*zSpeedFactor*MESSAGE_INTERVAL;
        
        if( acceleration.x > 0.5 ) {
            xAxis = xAxis; 
        } else if( acceleration.x < -0.5 ) {
            xAxis = -xAxis;
        }
        
        if( acceleration.y > 0.5 ) {
            yAxis = yAxis; 
        } else if( acceleration.y < -0.5 ) {
            yAxis = -yAxis;
        }
        
        if( acceleration.z > 0.5 ) {
            zAxis = zAxis; 
        } else if( acceleration.z < -0.5 ) {
            zAxis = -zAxis;
        }
        
        float finalSpeedFactor = MAX( zSpeedFactor, MAX(xSpeedFactor, ySpeedFactor));
        
        NSMutableString *message = [NSMutableString stringWithString: [NSString stringWithFormat:@"moveBy(%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f)", xAxis, yAxis, zAxis, 0.0, 0.0, 0.0, finalSpeedFactor]];
        [message appendString:@"\n"];
        
        //for test        
        NSLog(@"A: %.4f, %.4f, %.4f", acceleration.x, acceleration.y, acceleration.z);
        
        NSData *messageData = [message dataUsingEncoding:NSUTF8StringEncoding];
        NSLog(@"Sending: %@", message);
        //[listenSocket writeData:messageData withTimeout:-1 tag:ECHO_MSG]; //TCPIP
        [listenSocket sendData:messageData withTimeout:-1 tag:ECHO_MSG]; //UDP
        
        for(int i = 0; i < [connectedSockets count]; i++)
		{
			// Call disconnect on the socket,
			// which will invoke the onSocketDidDisconnect: method,
			// which will remove the socket from the list.
			//[[connectedSockets objectAtIndex:i] writeData:messageData withTimeout:-1 tag:ECHO_MSG];//TCPIP
            [[connectedSockets objectAtIndex:i] sendData:messageData withTimeout:-1 tag:ECHO_MSG]; //UDP
		}
    }
}

#pragma mark - TextFieldHelpers
- (BOOL)textFieldShouldReturn:(UITextField *)textField {
    [textField resignFirstResponder];
    return YES;
}


#pragma mark - Helpers
-(void)logMessage:(NSString *)msg {
    NSMutableString *logContent = [NSMutableString stringWithString:logWindow.text];
    [logContent appendString:msg];
    [logContent appendString:@"\r\n"];
    logWindow.text = logContent;
}

@end
