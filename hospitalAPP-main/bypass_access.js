// root_bypass.js - RootCheck 우회 스크립트
Java.perform(function() {
    console.log("[*] 루팅 탐지 우회 스크립트 시작");
    
    // ===============================
    // 1. RootCheck 클래스 후킹
    // ===============================
    try {
        var RootCheck = Java.use("com.android.hospitalAPP.RootCheck");
        
        // isDeviceRootedNative 메서드 오버라이드
        RootCheck.isDeviceRootedNative.implementation = function() {
            console.log("[*] RootCheck.isDeviceRootedNative() 호출됨");
            console.log("[*] 원래 결과: " + this.isDeviceRootedNative());
            console.log("[*] false로 변경하여 반환");
            return false; // 항상 false 반환
        };
        
        console.log("[✓] RootCheck.isDeviceRootedNative() 후킹 완료");
        
    } catch (e) {
        console.log("[!] RootCheck 클래스를 찾을 수 없음: " + e);
    }
    
    // ===============================
    // 2. 일반적인 루팅 탐지 우회
    // ===============================
    
    // isDeviceRooted 메서드 (있는 경우)
    try {
        var RootCheck = Java.use("com.android.hospitalAPP.RootCheck");
        if (RootCheck.isDeviceRooted) {
            RootCheck.isDeviceRooted.implementation = function() {
                console.log("[*] RootCheck.isDeviceRooted() 우회");
                return false;
            };
        }
    } catch (e) {
        console.log("[*] isDeviceRooted 메서드 없음");
    }
    
    // ===============================
    // 3. File 클래스 후킹 (루트 파일 탐지 우회)
    // ===============================
    try {
        var File = Java.use("java.io.File");
        File.exists.implementation = function() {
            var path = this.getAbsolutePath();
            
            // 루트 관련 파일 경로들
            var rootPaths = [
                "/sbin/su",
                "/system/bin/su",
                "/system/xbin/su",
                "/data/local/xbin/su",
                "/data/local/bin/su",
                "/system/sd/xbin/su",
                "/system/bin/failsafe/su",
                "/data/local/su",
                "/su/bin/su",
                "/system/app/Superuser.apk",
                "/system/app/SuperSU.apk",
                "/system/app/Magisk.apk"
            ];
            
            // 루트 파일 경로인 경우 false 반환
            if (rootPaths.some(rootPath => path.includes(rootPath))) {
                console.log("[*] 루트 파일 탐지 우회: " + path);
                return false;
            }
            
            return this.exists();
        };
        
        console.log("[✓] File.exists() 후킹 완료");
        
    } catch (e) {
        console.log("[!] File 클래스 후킹 실패: " + e);
    }
    
    // ===============================
    // 4. Runtime.exec 후킹 (su 명령어 실행 감지 우회)
    // ===============================
    try {
        var Runtime = Java.use("java.lang.Runtime");
        Runtime.exec.overload('[Ljava.lang.String;').implementation = function(command) {
            if (command && command[0] && command[0].toString().includes("su")) {
                console.log("[*] Runtime.exec 'su' 명령어 탐지, IOException 발생시킴");
                throw Java.use("java.io.IOException").$new("Command not found");
            }
            return this.exec(command);
        };
        
        console.log("[✓] Runtime.exec() 후킹 완료");
        
    } catch (e) {
        console.log("[!] Runtime.exec 후킹 실패: " + e);
    }
    
    // ===============================
    // 5. PackageManager 후킹 (루트 앱 탐지 우회)
    // ===============================
    try {
        var PackageManager = Java.use("android.content.pm.PackageManager");
        PackageManager.getPackageInfo.overload('java.lang.String', 'int').implementation = function(packageName, flags) {
            
            // 루트 관련 패키지들
            var rootPackages = [
                "com.noshufou.android.su",
                "com.thirdparty.superuser",
                "eu.chainfire.supersu",
                "com.koushikdutta.superuser",
                "com.zachspong.temprootremovejb",
                "com.ramdroid.appquarantine",
                "com.topjohnwu.magisk"
            ];
            
            if (rootPackages.includes(packageName)) {
                console.log("[*] 루트 패키지 탐지 우회: " + packageName);
                throw Java.use("android.content.pm.PackageManager$NameNotFoundException").$new();
            }
            
            return this.getPackageInfo(packageName, flags);
        };
        
        console.log("[✓] PackageManager.getPackageInfo() 후킹 완료");
        
    } catch (e) {
        console.log("[!] PackageManager 후킹 실패: " + e);
    }
    
    console.log("[*] 루팅 탐지 우회 스크립트 로딩 완료");
});