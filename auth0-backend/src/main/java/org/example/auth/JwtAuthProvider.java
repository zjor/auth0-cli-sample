package org.example.auth;

import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.web.authentication.preauth.PreAuthenticatedAuthenticationToken;

import java.util.Collections;
import java.util.List;

@Slf4j
public class JwtAuthProvider implements AuthenticationProvider {

    @Override
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        if (!supports(authentication.getClass())) {
            return null;
        }

        Object principal = authentication.getPrincipal();
        if (principal == null) {
            log.debug("No pre-authenticated principal found in request.");
            return null;
        }

        List<GrantedAuthority> grantedAuthorities = Collections.emptyList();

        PreAuthenticatedAuthenticationToken result = new PreAuthenticatedAuthenticationToken(principal,
                authentication.getCredentials(), grantedAuthorities);

        result.setDetails(authentication.getDetails());
        return result;
    }

    @Override
    public boolean supports(Class<?> authentication) {
        return PreAuthenticatedAuthenticationToken.class.isAssignableFrom(authentication);
    }
}
