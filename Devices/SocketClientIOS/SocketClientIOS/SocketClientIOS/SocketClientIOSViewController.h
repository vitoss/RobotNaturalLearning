//
//  EchoClientViewController.h
//  EchoClient
//
//  Created by Witold Wasilewski on 11-03-28.
//  Copyright 2011 Witold Wasilewski. All rights reserved.
//

#import <UIKit/UIKit.h>

//@class AsyncSocket; //tcpip
@class AsyncUdpSocket;

@interface SocketClientIOSViewController : UIViewController <UITextFieldDelegate, UIAccelerometerDelegate> {
    AsyncUdpSocket *listenSocket;
    NSMutableArray *connectedSockets;
    
    IBOutlet UITextView *logWindow;
    IBOutlet UITextField *ipField;
    IBOutlet UITextField *portField;
    
    IBOutlet UIButton *connectButton;
    IBOutlet UIButton *startSessionButotn;
    IBOutlet UIButton *recButton;
    
    BOOL isRunning;
    BOOL isPortBinded;
    
    UIAccelerometer *accelerometer;
}

-(IBAction) connectToServer: (id)sender;
-(IBAction) sendMessage: (id) sender;
-(IBAction) acceptConnection: (id)sender;

-(void) logMessage:(NSString *)msg;

@property (nonatomic,retain) IBOutlet UITextView *logWindow;
@property (nonatomic,retain) IBOutlet UITextField *ipField;
@property (nonatomic,retain) IBOutlet UITextField *messageField;
@property (nonatomic,retain) IBOutlet UITextField *portField;
@property (nonatomic,retain) IBOutlet UIButton *connectButton;
@property (nonatomic,retain) IBOutlet UIButton *recButton;
@property (nonatomic,retain) IBOutlet UIButton *startSessionButton;
@property (nonatomic, retain) IBOutlet UILabel *queueCount;
@property (nonatomic, retain) AsyncUdpSocket *listenSocket;
@property (nonatomic, retain) NSMutableArray *connectedSockets;

@property (nonatomic, retain) UIAccelerometer *accelerometer;

@end
