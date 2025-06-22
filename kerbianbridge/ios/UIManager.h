#import <Foundation/Foundation.h>

@interface UIManager : NSObject
- (NSInteger)createView:(NSString *)type props:(NSDictionary *)props;
@end