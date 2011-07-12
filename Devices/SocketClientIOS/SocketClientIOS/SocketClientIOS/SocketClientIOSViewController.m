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
    self.accelerometer.updateInterval = 0.25; //0.08
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
    /*labelX.text = [NSString stringWithFormat:@"%@%f", @"X: ", acceleration.x];
    labelY.text = [NSString stringWithFormat:@"%@%f", @"Y: ", acceleration.y];
    labelZ.text = [NSString stringWithFormat:@"%@%f", @"Z: ", acceleration.z];
    
    self.progressX.progress = ABS(acceleration.x);
    self.progressY.progress = ABS(acceleration.y);
    self.progressZ.progress = ABS(acceleration.z);*/
    if( isRunning ) {
        //[self logMessage:@"Send acceleration data."];
        NSMutableString *message = [NSMutableString stringWithString: [NSString stringWithFormat:@"move(%.2f,%.2f,%.2f,%.2f,%.2f,%.2f)", (acceleration.x+1)*180, (acceleration.y+1)*180, (acceleration.z+1)*180, 0, 0, 0]];
        [message appendString:@"\n"];
        
        //for test
        
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
