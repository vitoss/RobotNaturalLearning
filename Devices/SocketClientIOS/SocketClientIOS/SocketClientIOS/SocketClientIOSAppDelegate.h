//
//  EchoClientAppDelegate.h
//  EchoClient
//
//  Created by Muszu on 11-03-28.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@class SocketClientIOSViewController;

@interface SocketClientIOSAppDelegate : NSObject <UIApplicationDelegate> {

}

@property (nonatomic, retain) IBOutlet UIWindow *window;

@property (nonatomic, retain) IBOutlet SocketClientIOSViewController *viewController;

@end
